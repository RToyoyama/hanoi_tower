"""
main.py
=======
Entrypoint da aplicação — mantido intencionalmente simples.

Todo o comportamento está encapsulado no pacote torre_hanoi.
Este arquivo só faz a ponte entre o terminal e o pacote.
"""

from src.torre_hanoi.cli import run

if __name__ == "__main__":
    run()
