"""
cli.py
======
Interface de linha de comando — única responsabilidade: parsear args e iniciar o Jogo.

Os valores DEFAULT de cada flag vêm do config/config.yml via CONFIG.
O usuário pode sempre sobrescrever qualquer default via argumento CLI.
"""

from __future__ import annotations

import argparse
import sys

from config.config import CONFIG
from .jogo import ConfigJogo, Jogo

# Atalhos para não repetir CONFIG.* em todo lugar
_CJ = CONFIG.jogo
_CC = CONFIG.cli


def _build_parser() -> argparse.ArgumentParser:
    """Constrói e retorna o parser completo da CLI."""

    parser = argparse.ArgumentParser(
        prog="hanoi",
        description=(
            "🗼  Torre de Hanói — solução recursiva orientada a objetos\n\n"
            f"Move N discos da torre {_CJ.torre_origem} para a torre {_CJ.torre_destino} "
            f"usando {_CJ.torre_auxiliar} como auxiliar.\n"
            "Regra: nunca coloque um disco maior sobre um menor."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemplos:\n"
            "  python main.py 3\n"
            "  python main.py 5 --passo-a-passo\n"
            "  python main.py 4 --passo-a-passo --delay 0.3\n"
            "  python main.py 6 --sem-cor\n"
            "  python main.py 3 --so-movimentos\n"
        ),
    )

    # ---- Argumento posicional — usa discos_padrao do config como nargs opcional ----
    parser.add_argument(
        "discos",
        type=int,
        nargs="?",  # torna opcional
        default=_CJ.discos_padrao,  # ← vem do config.yml
        metavar="DISCOS",
        help=(
            f"Número de discos (padrão: {_CJ.discos_padrao}, "
            f"min: {_CJ.discos_minimo}, max: {_CJ.discos_maximo})"
        ),
    )

    # ---- Grupo: comportamento de execução ----
    exec_group = parser.add_argument_group("execução")
    exec_group.add_argument(
        "--passo-a-passo",
        "-p",
        action="store_true",
        default=_CC.passo_a_passo,  # ← vem do config.yml
        help=f"Exibe o estado das torres após cada movimento (padrão: {_CC.passo_a_passo})",
    )
    exec_group.add_argument(
        "--delay",
        "-d",
        type=float,
        default=_CC.delay_segundos,  # ← vem do config.yml
        metavar="SEG",
        help=f"Pausa em segundos entre passos (padrão: {_CC.delay_segundos})",
    )

    # ---- Grupo: saída ----
    out_group = parser.add_argument_group("saída")
    out_group.add_argument(
        "--sem-cor",
        action="store_true",
        default=not _CC.colorido,  # ← invertido do config.yml
        help=f"Desativa cores ANSI no terminal (padrão colorido: {_CC.colorido})",
    )
    out_group.add_argument(
        "--so-movimentos",
        action="store_true",
        default=_CC.so_movimentos,  # ← vem do config.yml
        help=f"Imprime apenas a lista de movimentos (padrão: {_CC.so_movimentos})",
    )

    return parser  # ← estava faltando


def _validar(args: argparse.Namespace, parser: argparse.ArgumentParser) -> None:
    """
    Valida entradas usando os limites definidos no config.yml.
    Nenhum valor hardcoded — tudo vem de CONFIG.jogo.
    """
    if args.discos < _CJ.discos_minimo:
        parser.error(f"DISCOS deve ser pelo menos {_CJ.discos_minimo}.")
    if args.discos > _CJ.discos_maximo:
        parser.error(
            f"{args.discos} discos = {2**args.discos - 1:,} movimentos. "
            f"Use no máximo {_CJ.discos_maximo} (configurado em config/config.yml)."
        )
    if args.delay < 0:
        parser.error("--delay não pode ser negativo.")


def _build_config(args: argparse.Namespace) -> ConfigJogo:
    """
    Traduz o Namespace do argparse para um ConfigJogo tipado.
    Prioridade: argumento CLI > config.yml (defaults já aplicados pelo argparse).
    """
    return ConfigJogo(
        n_discos=args.discos,
        passo_a_passo=args.passo_a_passo,
        delay=args.delay,
        colorido=not args.sem_cor,
        silencioso=args.so_movimentos,
    )


def _imprimir_movimentos(jogo: Jogo) -> None:
    """Exibe a lista de movimentos quando --so-movimentos está ativo."""
    prec = CONFIG.log.precisao_tempo
    print(f"\n📋 Lista de movimentos ({jogo.total_movimentos:,}):\n")
    for mov in jogo.movimentos:
        print(f"  {mov}")
    print(f"\n  Tempo: {jogo.duracao:.{prec}f}s\n")


def run() -> None:
    """
    Ponto de entrada da CLI.
    Chamada pelo main.py — mantém __main__ limpo.
    """
    parser = _build_parser()
    args = parser.parse_args()

    _validar(args, parser)

    config = _build_config(args)
    jogo = Jogo(config)

    try:
        jogo.iniciar()
    except KeyboardInterrupt:
        print("\n\nInterrompido pelo usuário.")
        sys.exit(0)

    if args.so_movimentos:
        _imprimir_movimentos(jogo)
