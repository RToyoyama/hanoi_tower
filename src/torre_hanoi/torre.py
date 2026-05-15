"""
torre.py
========
Representa uma das três torres do jogo.

Conceitos OOP abordados:
  - Composição: Torre contém Discos
  - Encapsulamento: estado interno protegido
  - Exceções customizadas para erros de domínio
  - __len__, __iter__, __repr__ — protocolo de container
  - @property para acesso seguro ao estado
"""

from __future__ import annotations
from typing import Iterator
from .disco import Disco


# Exceções de domínio — erros com semântica do negócio, não genéricos
class TorreVaziaError(Exception):
    """Tentativa de remover disco de uma torre vazia."""


class MovimentoInvalidoError(Exception):
    """Tentativa de colocar disco maior sobre disco menor."""


# Clsse Torre


class Torre:
    """
    Pilha de discos que representa uma haste da Torre de Hanói.

    Internamente usa uma lista como pilha (LIFO):
      - topo = último elemento (_pilha[-1])
      - empilha com _pilha.append()
      - desempilha com _pilha.pop()

    Args:
        nome: identificador da torre ("A", "B" ou "C")
    """

    def __init__(self, nome: str) -> None:
        self._nome: str = nome
        self._pilha: list[Disco] = []

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def topo(self) -> Disco | None:
        """Retorna o disco do topo sem removê-lo, ou None se vazia."""
        return self._pilha[-1] if self._pilha else None

    @property
    def vazia(self) -> bool:
        return len(self._pilha) == 0

    @property
    def discos(self) -> list[Disco]:
        """Snapshot imutável da pilha (não expõe referência interna)."""
        return list(self._pilha)

    def empilhar(self, disco: Disco) -> None:
        """
        Coloca um disco no topo da torre.

        Raises:
            MovimentoInvalidoError: se o disco for maior que o topo atual.
        """
        if self.topo is not None and disco > self.topo:
            raise MovimentoInvalidoError(
                f"Torre {self._nome}: disco {disco} é maior que o topo {self.topo}. "
                "Movimento inválido!"
            )
        self._pilha.append(disco)

    def desempilhar(self) -> Disco:
        """
        Remove e retorna o disco do topo.

        Raises:
            TorreVaziaError: se a torre não tiver discos.
        """
        if self.vazia:
            raise TorreVaziaError(
                f"Torre {self._nome} está vazia — não há disco para remover."
            )
        return self._pilha.pop()

    def carregar(self, n: int) -> None:
        """
        Preenche a torre com n discos (tamanho n até 1).
        Usado na inicialização do jogo.

        Args:
            n: número de discos a adicionar (maior embaixo).
        """
        self._pilha = [Disco(tamanho) for tamanho in range(n, 0, -1)]

    def __len__(self) -> int:
        return len(self._pilha)

    def __iter__(self) -> Iterator[Disco]:
        """Itera do fundo para o topo."""
        return iter(self._pilha)

    def __repr__(self) -> str:
        return f"Torre(nome={self._nome!r}, discos={self._pilha!r})"

    def __str__(self) -> str:
        discos_str = ", ".join(str(d) for d in reversed(self._pilha))
        return f"Torre {self._nome}: [{discos_str}]"
