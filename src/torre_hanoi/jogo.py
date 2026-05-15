"""
jogo.py
=======
Orquestra o jogo completo: inicialização, resolução recursiva e estado.

Conceitos OOP abordados:
  - Classe principal que agrega (composição) Torre e Visualizador
  - Estado interno encapsulado: _torres, _movimentos, _resolvido
  - Separação entre configuração (__init__) e execução (resolver())
  - Callback como parâmetro — inversão de controle leve
  - @property para expor estado sem permitir mutação direta
  - Método privado vs. público — convenção _ no Python
"""

from __future__ import annotations
import time
from dataclasses import dataclass, field
from config.config import CONFIG
from .disco import Disco
from .torre import Torre, MovimentoInvalidoError
from .visualizador import Visualizador

# Dataclass para registrar cada movimento — imutável, comparável, printável


@dataclass(frozen=True)  # frozen=True → instância imutável
class Movimento:
    """Registro de um único passo do algoritmo."""

    passo: int
    tamanho_disco: int
    origem: str
    destino: str

    def __str__(self) -> str:
        return f"{self.passo:>6}. disco {self.tamanho_disco}  {self.origem} → {self.destino}"


# Classe principal


@dataclass
class ConfigJogo:
    """
    Parâmetros de configuração do jogo.

    Usar dataclass aqui evita um __init__ cheio de argumentos na classe Jogo
    e documenta os parâmetros de forma clara.
    """

    n_discos: int
    passo_a_passo: bool = False
    delay: float = 0.0
    colorido: bool = True
    silencioso: bool = False  # se True, não exibe nenhuma visualização


class Jogo:
    """
    Orquestra o ciclo de vida completo de uma partida de Torre de Hanói.

    Responsabilidades:
      1. Inicializar as três torres com os discos corretos
      2. Executar o algoritmo recursivo
      3. Delegar a renderização ao Visualizador
      4. Manter o histórico de movimentos

    Args:
        config: objeto ConfigJogo com todos os parâmetros da partida
    """

    # Lidos do config.yml — não hardcoded
    TORRE_ORIGEM = CONFIG.jogo.torre_origem
    TORRE_DESTINO = CONFIG.jogo.torre_destino
    TORRE_AUX = CONFIG.jogo.torre_auxiliar

    def __init__(self, config: ConfigJogo) -> None:
        self._cfg = config

        # Composição: Jogo possui Torres
        self._torres: dict[str, Torre] = {
            "A": Torre("A"),
            "B": Torre("B"),
            "C": Torre("C"),
        }

        # Composição: Jogo possui Visualizador
        self._vis = Visualizador(config.n_discos, colorido=config.colorido)

        # Estado interno
        self._movimentos: list[Movimento] = []
        self._resolvido: bool = False
        self._duracao: float = 0.0

        # Prepara estado inicial: todos os discos na torre A
        self._torres["A"].carregar(config.n_discos)

    # ------------------------------------------------------------------
    # Propriedades — acesso seguro ao estado interno
    # ------------------------------------------------------------------

    @property
    def movimentos(self) -> list[Movimento]:
        """Lista somente-leitura dos movimentos realizados."""
        return list(self._movimentos)

    @property
    def total_movimentos(self) -> int:
        return len(self._movimentos)

    @property
    def resolvido(self) -> bool:
        return self._resolvido

    @property
    def duracao(self) -> float:
        """Tempo de execução em segundos."""
        return self._duracao

    @property
    def torres(self) -> dict[str, Torre]:
        """Snapshot do estado atual das torres."""
        return dict(self._torres)

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def iniciar(self) -> None:
        """
        Ponto de entrada: exibe cabeçalho, resolve e exibe resultado.
        Orquestra o fluxo completo da partida.
        """
        if not self._cfg.silencioso:
            Visualizador.cabecalho(self._cfg.n_discos)
            if not self._cfg.passo_a_passo:
                self._vis.renderizar(self._torres, titulo="📐 Estado inicial:")

        inicio = time.perf_counter()
        self._resolver(
            n=self._cfg.n_discos,
            origem=self.TORRE_ORIGEM,
            destino=self.TORRE_DESTINO,
            auxiliar=self.TORRE_AUX,
        )
        self._duracao = time.perf_counter() - inicio
        self._resolvido = True

        if not self._cfg.silencioso:
            self._vis.renderizar(self._torres, titulo="✅  Estado final:")
            self._vis.resumo_final(self.total_movimentos, self._duracao)

    # ------------------------------------------------------------------
    # Algoritmo recursivo — método PRIVADO (detalhe de implementação)
    # ------------------------------------------------------------------

    def _resolver(self, n: int, origem: str, destino: str, auxiliar: str) -> None:
        """
        Implementação recursiva da Torre de Hanói.

        Lógica (dividir para conquistar):
          1. Move N-1 discos: origem → auxiliar
          2. Move disco N:    origem → destino    ← única ação "real"
          3. Move N-1 discos: auxiliar → destino

        O caso base (n == 0) retorna sem fazer nada.

        Args:
            n:        número de discos a mover nesta chamada
            origem:   torre de onde partem os discos
            destino:  torre para onde vão os discos
            auxiliar: torre usada como espaço temporário
        """
        if n == 0:
            return

        # Passo 1 — subproblema: libera espaço no destino
        self._resolver(n - 1, origem, auxiliar, destino)

        # Passo 2 — caso base: move o disco maior disponível
        self._mover(origem, destino)

        # Passo 3 — subproblema: empilha os N-1 sobre o maior
        self._resolver(n - 1, auxiliar, destino, origem)

    def _mover(self, origem: str, destino: str) -> None:
        """
        Executa e registra um único movimento físico de disco.

        Args:
            origem:  nome da torre de origem
            destino: nome da torre de destino

        Raises:
            MovimentoInvalidoError: se o movimento violar as regras
        """
        disco: Disco = self._torres[origem].desempilhar()
        self._torres[destino].empilhar(disco)  # valida a regra internamente

        movimento = Movimento(
            passo=len(self._movimentos) + 1,
            tamanho_disco=disco.tamanho,
            origem=origem,
            destino=destino,
        )
        self._movimentos.append(movimento)

        if self._cfg.passo_a_passo and not self._cfg.silencioso:
            self._vis.renderizar_movimento(
                torres=self._torres,
                passo=movimento.passo,
                tamanho_disco=disco.tamanho,
                origem=origem,
                destino=destino,
            )
            if self._cfg.delay > 0:
                time.sleep(self._cfg.delay)
