"""Auxiliar para localizar recursos em desenvolvimento e em modo empacotado."""

from __future__ import annotations

import os
import sys


def resource_path(relativo: str) -> str:
    """Resolve o caminho absoluto de um recurso do projeto.

    Em modo congelado (PyInstaller), os dados empacotados ficam em
    ``sys._MEIPASS``. Em desenvolvimento, o caminho é resolvido em
    relação à raiz do projeto (um nível acima do pacote).
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relativo)
