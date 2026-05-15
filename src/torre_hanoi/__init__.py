"""
torre_hanoi
===========
Pacote que implementa a Torre de Hanói orientada a objetos.

Exporta apenas o necessário para uso externo — o resto é detalhe interno.
"""

from .disco import Disco
from .torre import Torre, TorreVaziaError, MovimentoInvalidoError
from .jogo import Jogo, ConfigJogo, Movimento
from .visualizador import Visualizador

__all__ = [
    "Disco",
    "Torre",
    "TorreVaziaError",
    "MovimentoInvalidoError",
    "Jogo",
    "ConfigJogo",
    "Movimento",
    "Visualizador",
]
