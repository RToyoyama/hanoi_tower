"""
visualizador.py
===============
Renderização das torres no terminal.

Agora lê TODAS as configurações visuais de CONFIG.visual e CONFIG.log —
nenhum valor hardcoded.
"""

from __future__ import annotations
from typing import TYPE_CHECKING
from config.config import CONFIG

if TYPE_CHECKING:
    from .torre import Torre

_V = CONFIG.visual  # atalho local — evita repetir CONFIG.visual em todo lugar
_L = CONFIG.log
_RESET = "\033[0m"
_NEGRITO = "\033[1m"


class Visualizador:
    """
    Responsável exclusivamente por renderizar o estado do jogo no terminal.

    Todos os caracteres, cores e flags de exibição vêm de CONFIG —
    mudar o config.yml muda o visual sem tocar nesta classe.

    Args:
        n_discos: número total de discos (define a altura máxima do desenho)
        colorido: sobrescreve CONFIG.cli.colorido se passado explicitamente
    """

    def __init__(self, n_discos: int, colorido: bool | None = None) -> None:
        self._n = n_discos
        self._colorido = colorido if colorido is not None else CONFIG.cli.colorido
        self._largura_disco = n_discos * 2 + 1
        self._largura_col = self._largura_disco + 4

    def renderizar(self, torres: dict[str, "Torre"], titulo: str = "") -> None:
        if titulo:
            print(f"\n{self._negrito(titulo)}")
        for linha in self._construir_linhas(torres):
            print(linha)
        print(self._separador())
        print(self._rotulos())

    def renderizar_movimento(
        self,
        torres: dict[str, "Torre"],
        passo: int,
        tamanho_disco: int,
        origem: str,
        destino: str,
    ) -> None:
        corpo = _V.char_disco * tamanho_disco
        bracket_e = _V.char_bracket_esq
        bracket_d = _V.char_bracket_dir
        cor = self._cor_disco(tamanho_disco)
        reset = _RESET if self._colorido else ""

        titulo = (
            f"── Passo {passo}: disco {cor}{bracket_e}{corpo}{bracket_d}{reset}"
            f"  {self._negrito(origem)} → {self._negrito(destino)} ──"
        )
        self.renderizar(torres, titulo)

    def resumo_final(self, total_movimentos: int, duracao: float) -> None:
        if not _L.mostrar_estatisticas:
            return
        prec = _L.precisao_tempo
        print(f"\n  Total de movimentos : {total_movimentos:,}")
        print(f"  Tempo de cálculo    : {duracao:.{prec}f}s")
        print(f"  {'═' * 40}")

    @staticmethod
    def cabecalho(n: int) -> None:
        if not _L.mostrar_cabecalho:
            return
        total = 2**n - 1
        print(f"\n{'═' * 50}")
        print(f"  🗼  TORRE DE HANÓI  —  {n} disco(s)")
        print(f"  Movimentos necessários: {total:,}")
        print(f"{'═' * 50}")

    # Privados

    def _construir_linhas(self, torres: dict[str, "Torre"]) -> list[str]:
        linhas: list[str] = []
        for nivel in range(self._n, 0, -1):
            partes: list[str] = []
            for nome in _V.rotulos:
                discos = torres[nome].discos
                if nivel <= len(discos):
                    partes.append(self._celula_disco(discos[nivel - 1].tamanho))
                else:
                    partes.append(self._celula_vazia())
            linhas.append("".join(partes))
        return linhas

    def _celula_disco(self, tamanho: int) -> str:
        corpo = _V.char_disco * tamanho
        bracket_e = _V.char_bracket_esq
        bracket_d = _V.char_bracket_dir
        segmento = f"{bracket_e}{corpo:^{self._largura_disco - 2}}{bracket_d}"
        cor = self._cor_disco(tamanho)
        reset = _RESET if self._colorido else ""
        return f"{cor}{segmento:^{self._largura_col}}{reset}"

    def _celula_vazia(self) -> str:
        return f"{_V.char_poste:^{self._largura_col}}"

    def _separador(self) -> str:
        return _V.char_separador * (self._largura_col * 3)

    def _rotulos(self) -> str:
        return "".join(f"{'  ' + r:^{self._largura_col}}" for r in _V.rotulos)

    def _cor_disco(self, tamanho: int) -> str:
        return _V.cor_ansi(tamanho - 1) if self._colorido else ""

    def _negrito(self, texto: str) -> str:
        return f"{_NEGRITO}{texto}{_RESET}" if self._colorido else texto
