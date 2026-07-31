"""Janela Sobre (migração da janela FAbout do projeto original)."""

from __future__ import annotations

import tkinter as tk
import webbrowser

import ttkbootstrap as ttkb

from . import __title__, __url__
from .geometry import centralizar_janela
from .i18n import TEXTO_LICENCA, t
from .resources import resource_path


class AboutWindow(ttkb.Toplevel):
    """Janela modal com informações e licença do aplicativo."""

    def __init__(self, master: tk.Misc | None = None) -> None:
        super().__init__(master)
        self.title(t("about.title"))
        self.resizable(False, False)
        if master is not None:
            self.transient(master)
        self.grab_set()

        self._icon = self._carregar_icone()

        self._construir_widgets()
        centralizar_janela(self, master)

    def _carregar_icone(self) -> tk.PhotoImage | None:
        try:
            icone = tk.PhotoImage(file=resource_path("images/mikeygenerator.png"))
            self.iconphoto(False, icone)
            return icone
        except tk.TclError:
            return None

    def _construir_widgets(self) -> None:
        frame = ttkb.Frame(self)
        frame.pack(padx=16, pady=12, fill="both", expand=True)

        ttkb.Label(
            frame, text=__title__, font=("TkDefaultFont", 16, "bold")
        ).pack(anchor="w", pady=(0, 2))
        ttkb.Label(frame, text=t("app.description")).pack(anchor="w", pady=(0, 8))
        ttkb.Label(frame, text=t("about.developed_by")).pack(anchor="w")

        linha_site = ttkb.Frame(frame)
        linha_site.pack(anchor="w")
        ttkb.Label(linha_site, text=t("about.site") + " ").pack(side="left")
        ttkb.Button(
            linha_site,
            text=__url__,
            bootstyle="link",
            command=lambda: webbrowser.open(__url__),
        ).pack(side="left")

        ttkb.Label(frame, text=t("about.license")).pack(anchor="w", pady=(4, 0))
        ttkb.Label(frame, text=t("about.copyright")).pack(anchor="w")

        cores = self.style.colors
        texto = tk.Text(
            frame,
            wrap="word",
            height=10,
            width=70,
            relief="solid",
            borderwidth=1,
            font=("TkDefaultFont", 9),
            background=cores.bg,
            foreground=cores.fg,
        )
        texto.insert("1.0", TEXTO_LICENCA)
        texto.configure(state="disabled")
        texto.pack(pady=(12, 0), fill="both", expand=True)
