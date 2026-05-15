"""
disco.py
=======

Rpresenta um disco da torre de Hanói

Conceitos OOP abordados:
Emcapsulamento com @property
__repr__  e __str__ para legitibilidade
__eq__, __lt__ para comparacoes naturais (dunder methods)
Imutabilidade via propriedade somente-leitura
"""


class Disco:
    """
    Representa um disco com tamanho imutável.

    O tamanho define a hierarquia: disco maior NUNCA pode
    ser colocado sobre disco menor — regra central do jogo.

    Attributes:
        _tamanho (int): largura do disco (imutável após criação)
    """

    def __init__(self, tamanho: int) -> None:
        """
        Args:
            tamanho: inteiro positivo que representa a largura do disco.

        Raises:
            ValueError: se tamanho não for inteiro positivo.
        """
        if not isinstance(tamanho, int) or tamanho < 1:
            raise ValueError(
                f"Tamanho do disco deve ser inteiro positivo, recebeu: {tamanho!r}"
            )
        self._tamanho = tamanho

    @property
    def tamanho(self) -> int:
        return self._tamanho

    def __repr__(self) -> str:
        return f"Disco(tamanho={self._tamanho})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Disco):
            return NotImplemented
        return self._tamanho == other._tamanho

    def __lt__(self, other: "Disco") -> bool:
        return self._tamanho < other._tamanho

    def __hash__(self) -> int:
        return hash(self._tamanho)
