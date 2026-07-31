"""Funções utilitárias de geometria para janelas Tk."""

from __future__ import annotations

import tkinter as tk


def centralizar_janela(
    janela: tk.Tk | tk.Toplevel,
    master: tk.Misc | None = None,
) -> None:
    """Centraliza a janela na tela (ou sobre a janela ``master``).

    Deve ser chamado após a construção dos widgets e do cálculo do
    layout (``update_idletasks``), para que as dimensões reais da
    janela já sejam conhecidas. A posição é limitada para que a janela
    permaneça visível na tela.
    """
    janela.update_idletasks()
    largura = janela.winfo_reqwidth()
    altura = janela.winfo_reqheight()

    if master is not None and master.winfo_ismapped():
        base_x = master.winfo_rootx()
        base_y = master.winfo_rooty()
        base_largura = master.winfo_width()
        base_altura = master.winfo_height()
        x = base_x + (base_largura - largura) // 2
        y = base_y + (base_altura - altura) // 2
    else:
        x = (janela.winfo_screenwidth() - largura) // 2
        y = (janela.winfo_screenheight() - altura) // 2

    x = max(0, min(x, janela.winfo_screenwidth() - largura))
    y = max(0, min(y, janela.winfo_screenheight() - altura))
    janela.geometry(f"+{x}+{y}")
