#!/usr/bin/env python3
"""Ponto de entrada do MiKeyGenerator.

Uso:
    python3 main.py
"""

import os
import sys

# Garante que o pacote local seja importável ao executar a partir da raiz
# do projeto (também usado pelo PyInstaller).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mikeygenerator.main_window import MainWindow  # noqa: E402


def main() -> None:
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()
