"""
config/config.py
================
Lê o config/config.yml e expõe objetos tipados para o resto do projeto.

Fluxo:
  config.yml  →  _carregar_yaml()  →  dataclasses tipadas  →  CONFIG (singleton)

Uso em qualquer módulo:
  from config.config import CONFIG

  n_max = CONFIG.jogo.discos_maximo
  delay = CONFIG.cli.delay_segundos
  cor   = CONFIG.visual.cores_discos[0]

Conceitos Python:
  - @dataclass com tipagem estrita
  - Singleton via módulo (o Python cacheia imports)
  - pathlib.Path para caminhos portáveis (Windows/Linux/Mac)
  - yaml.safe_load — nunca yaml.load (evita execução arbitrária)
  - Falha rápida com mensagem clara (fail-fast)
"""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import yaml

# Localização do arquivo — sempre relativo a este próprio arquivo

# Independente de onde o processo é iniciado (raiz do projeto, subpasta, etc.),
# Path(__file__).parent aponta para config/ e resolve o yml corretamente.

_CONFIG_PATH = Path(__file__).parent / "config.yml"


# Dataclasses — uma por seção do YAML


@dataclass
class ConfigJogo:
    """Seção [jogo] do config.yml."""

    discos_padrao: int
    discos_maximo: int
    discos_minimo: int
    torre_origem: str
    torre_destino: str
    torre_auxiliar: str


@dataclass
class ConfigCli:
    """Seção [cli] do config.yml."""

    passo_a_passo: bool
    delay_segundos: float
    colorido: bool
    so_movimentos: bool


@dataclass
class ConfigVisual:
    """Seção [visual] do config.yml."""

    cores_discos: list[str]
    char_disco: str
    char_poste: str
    char_bracket_esq: str
    char_bracket_dir: str
    char_separador: str
    rotulos: list[str]

    def cor_ansi(self, index: int) -> str:
        """
        Retorna o código ANSI completo para o disco no índice dado.

        O config.yml armazena só o número (ex: "91m").
        Este método monta o escape completo: \\033[91m

        Args:
            index: índice do disco (ciclado via módulo)

        Returns:
            String de escape ANSI ou string vazia se lista vazia.
        """
        if not self.cores_discos:
            return ""
        codigo = self.cores_discos[index % len(self.cores_discos)]
        return f"\033[{codigo}"


@dataclass
class ConfigLog:
    """Seção [log] do config.yml."""

    mostrar_cabecalho: bool
    mostrar_estado_inicial: bool
    mostrar_estado_final: bool
    mostrar_estatisticas: bool
    precisao_tempo: int


@dataclass
class Config:
    """
    Configuração completa da aplicação.

    Agrega todas as seções do config.yml em um único objeto raiz.
    Acesse via CONFIG (singleton definido no final deste módulo).
    """

    jogo: ConfigJogo
    cli: ConfigCli
    visual: ConfigVisual
    log: ConfigLog


# Funções de parsing — cada seção tem sua própria função


def _parse_jogo(data: dict[str, Any]) -> ConfigJogo:
    return ConfigJogo(
        discos_padrao=int(data["discos_padrao"]),
        discos_maximo=int(data["discos_maximo"]),
        discos_minimo=int(data["discos_minimo"]),
        torre_origem=str(data["torre_origem"]),
        torre_destino=str(data["torre_destino"]),
        torre_auxiliar=str(data["torre_auxiliar"]),
    )


def _parse_cli(data: dict[str, Any]) -> ConfigCli:
    return ConfigCli(
        passo_a_passo=bool(data["passo_a_passo"]),
        delay_segundos=float(data["delay_segundos"]),
        colorido=bool(data["colorido"]),
        so_movimentos=bool(data["so_movimentos"]),
    )


def _parse_visual(data: dict[str, Any]) -> ConfigVisual:
    return ConfigVisual(
        cores_discos=list(data["cores_discos"]),
        char_disco=str(data["char_disco"]),
        char_poste=str(data["char_poste"]),
        char_bracket_esq=str(data["char_bracket_esq"]),
        char_bracket_dir=str(data["char_bracket_dir"]),
        char_separador=str(data["char_separador"]),
        rotulos=list(data["rotulos"]),
    )


def _parse_log(data: dict[str, Any]) -> ConfigLog:
    return ConfigLog(
        mostrar_cabecalho=bool(data["mostrar_cabecalho"]),
        mostrar_estado_inicial=bool(data["mostrar_estado_inicial"]),
        mostrar_estado_final=bool(data["mostrar_estado_final"]),
        mostrar_estatisticas=bool(data["mostrar_estatisticas"]),
        precisao_tempo=int(data["precisao_tempo"]),
    )


# Loader principal


def _carregar_yaml(path: Path) -> Config:
    """
    Lê o config.yml e devolve um objeto Config completamente tipado.

    Falha imediatamente (fail-fast) se:
      - O arquivo não existir
      - O YAML for inválido
      - Uma chave obrigatória estiver faltando

    Args:
        path: caminho absoluto para o config.yml

    Returns:
        Config populado com todos os valores do arquivo.

    Raises:
        FileNotFoundError: arquivo não encontrado
        KeyError: chave obrigatória ausente no YAML
        yaml.YAMLError: YAML malformado
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Arquivo de configuração não encontrado: {path}\n"
            "Verifique se config/config.yml existe na raiz do projeto."
        )

    with path.open(encoding="utf-8") as f:
        raw: dict[str, Any] = yaml.safe_load(f)

    try:
        return Config(
            jogo=_parse_jogo(raw["jogo"]),
            cli=_parse_cli(raw["cli"]),
            visual=_parse_visual(raw["visual"]),
            log=_parse_log(raw["log"]),
        )
    except KeyError as exc:
        raise KeyError(
            f"Chave obrigatória ausente no config.yml: {exc}\n"
            "Verifique se todas as seções (jogo, cli, visual, log) estão presentes."
        ) from exc


# Singleton — carregado uma única vez no import

# O Python cacheia módulos: qualquer `from config.config import CONFIG`
# em qualquer arquivo do projeto recebe o mesmo objeto em memória.

CONFIG: Config = _carregar_yaml(_CONFIG_PATH)
