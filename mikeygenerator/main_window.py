"""Janela principal (migração da janela FMain do projeto original)."""

from __future__ import annotations

import tkinter as tk
import webbrowser
from tkinter import filedialog, messagebox

import ttkbootstrap as ttkb

from . import __support_url__, __title__
from .about_window import AboutWindow
from .config import obter_tema, salvar_tema
from .geometry import centralizar_janela
from .i18n import t
from .keygen import (
    ALGORITMO_PADRAO,
    ALGORITMOS,
    ajustar_valor,
    calcular_hash,
    gerar_chave,
)
from .resources import resource_path

# Temas do ttkbootstrap (claro e escuro) usados pelo aplicativo.
_TEMA_CLARO = "bootstrap-light"
_TEMA_ESCURO = "bootstrap-dark"
_TEMA_PADRAO = _TEMA_CLARO

_ATRASO_GERACAO_MS = 500


class MainWindow(ttkb.Window):
    """Janela principal do MiKeyGenerator."""

    def __init__(self) -> None:
        tema = obter_tema(_TEMA_PADRAO)
        super().__init__(title=__title__, themename=tema, resizable=(False, False))
        self._tema_var = tk.StringVar(value=tema)

        self._icon = self._carregar_icone()
        self._construir_menu()
        self._construir_widgets()
        self._inicializar_valores()
        centralizar_janela(self)

    # ------------------------------------------------------------------ UI

    def _carregar_icone(self) -> tk.PhotoImage | None:
        try:
            icone = tk.PhotoImage(file=resource_path("images/mikeygenerator.png"))
            self.iconphoto(False, icone)
            return icone
        except tk.TclError:
            return None

    def _construir_menu(self) -> None:
        barra = tk.Menu(self)

        menu_arquivo = tk.Menu(barra, tearoff=0)
        menu_arquivo.add_command(
            label=t("menu.save"),
            command=self._salvar,
            accelerator="Ctrl+S",
            state=tk.DISABLED,
        )
        menu_arquivo.add_separator()
        menu_arquivo.add_command(
            label=t("menu.quit"),
            command=self._sair,
            accelerator="Alt+F4",
        )
        barra.add_cascade(label=t("menu.file"), menu=menu_arquivo)

        menu_tema = tk.Menu(barra, tearoff=0)
        menu_tema.add_radiobutton(
            label=t("theme.light"),
            value=_TEMA_CLARO,
            variable=self._tema_var,
            command=self._aplicar_tema,
        )
        menu_tema.add_radiobutton(
            label=t("theme.dark"),
            value=_TEMA_ESCURO,
            variable=self._tema_var,
            command=self._aplicar_tema,
        )
        barra.add_cascade(label=t("menu.theme"), menu=menu_tema)

        menu_sobre = tk.Menu(barra, tearoff=0)
        menu_sobre.add_command(label=t("menu.support"), command=self._apoie)
        menu_sobre.add_separator()
        menu_sobre.add_command(label=t("menu.about_app"), command=self._sobre)
        barra.add_cascade(label=t("menu.about"), menu=menu_sobre)

        self.config(menu=barra)
        self._menu_arquivo = menu_arquivo

        self.bind_all("<Control-s>", lambda _e: self._salvar())
        self.bind_all("<Control-S>", lambda _e: self._salvar())
        self.bind_all("<Alt-F4>", lambda _e: self._sair())
        self.protocol("WM_DELETE_WINDOW", self._sair)

    def _construir_widgets(self) -> None:
        frame = ttkb.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        self.lbl_tipo_hash = ttkb.Label(
            frame, text=t("hash_type"), font=("TkDefaultFont", 10, "bold")
        )
        self.lbl_tipo_hash.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 2))

        self.cbo_tipo_hash = ttkb.Combobox(
            frame, values=list(ALGORITMOS), state="readonly", width=22
        )
        self.cbo_tipo_hash.grid(row=1, column=0, columnspan=3, sticky="we", pady=(0, 8))
        self.cbo_tipo_hash.set(ALGORITMO_PADRAO)

        self.lbl_segmentos = ttkb.Label(
            frame, text=t("segment_size"), font=("TkDefaultFont", 10, "bold")
        )
        self.lbl_segmentos.grid(row=2, column=0, sticky="w", pady=(0, 2))

        self.txt_segmentos = ttkb.Spinbox(frame, from_=1, to=99, width=8)
        self.txt_segmentos.grid(row=3, column=0, sticky="w", pady=(0, 8))

        self.lbl_tamanho = ttkb.Label(
            frame, text=t("key_size"), font=("TkDefaultFont", 10, "bold")
        )
        self.lbl_tamanho.grid(row=4, column=0, sticky="w", pady=(0, 2))

        self.txt_tamanho = ttkb.Spinbox(frame, from_=1, to=99, width=8)
        self.txt_tamanho.grid(row=5, column=0, sticky="w", pady=(0, 8))

        self.btn_gerar = ttkb.Button(
            frame,
            text=t("generate"),
            command=self._gerar,
            width=20,
            bootstyle="success",
        )
        self.btn_gerar.grid(row=6, column=0, columnspan=3, sticky="we", pady=(4, 8))

        self.lbl_chave = ttkb.Label(
            frame, text=t("activation_key"), font=("TkDefaultFont", 10, "bold")
        )
        self.lbl_chave.grid(row=7, column=0, columnspan=3, sticky="w", pady=(0, 2))

        self.txt_key = ttkb.Entry(frame, state="readonly", width=42)
        self.txt_key.grid(row=8, column=0, columnspan=2, sticky="we")

        self.btn_copiar1 = ttkb.Button(
            frame,
            text=t("copy"),
            command=self._copiar_chave,
            width=8,
            bootstyle="info-outline",
        )
        self.btn_copiar1.grid(row=8, column=2, padx=(8, 0))

        self.lbl_hash = ttkb.Label(
            frame, text=t("hash"), font=("TkDefaultFont", 10, "bold")
        )
        self.lbl_hash.grid(row=9, column=0, columnspan=3, sticky="w", pady=(8, 2))

        self.txt_hash = ttkb.Entry(frame, state="readonly", width=42)
        self.txt_hash.grid(row=10, column=0, columnspan=2, sticky="we")

        self.btn_copiar2 = ttkb.Button(
            frame,
            text=t("copy"),
            command=self._copiar_hash,
            width=8,
            bootstyle="info-outline",
        )
        self.btn_copiar2.grid(row=10, column=2, padx=(8, 0))

    def _inicializar_valores(self) -> None:
        # Valores padrão do Form_Open() do original.
        self.txt_segmentos.delete(0, tk.END)
        self.txt_segmentos.insert(0, "5")
        self.txt_tamanho.delete(0, tk.END)
        self.txt_tamanho.insert(0, "5")

    # ------------------------------------------------------------- ações

    def _aplicar_tema(self) -> None:
        tema = self._tema_var.get()
        self.style.theme_use(tema)
        salvar_tema(tema)

    def _obter_valor(self, spinbox: ttkb.Spinbox) -> int:
        try:
            return ajustar_valor(int(spinbox.get()))
        except (ValueError, tk.TclError):
            return 1

    def _definir_campo(self, entry: ttkb.Entry, valor: str) -> None:
        entry.configure(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, valor)
        entry.configure(state="readonly")

    def _gerar(self) -> None:
        segmentos = self._obter_valor(self.txt_segmentos)
        tamanho = self._obter_valor(self.txt_tamanho)

        # Normaliza os campos exibidos (mesmo comportamento do original).
        for spinbox, valor in (
            (self.txt_segmentos, segmentos),
            (self.txt_tamanho, tamanho),
        ):
            spinbox.delete(0, tk.END)
            spinbox.insert(0, str(valor))

        self.btn_gerar.configure(state=tk.DISABLED)
        self._definir_campo(self.txt_key, t("generating"))
        self._definir_campo(self.txt_hash, t("generating"))

        # Equivalente ao "Wait 0.5" do original, sem congelar a interface.
        self.after(_ATRASO_GERACAO_MS, lambda: self._completar_geracao(segmentos, tamanho))

    def _completar_geracao(self, segmentos: int, tamanho: int) -> None:
        chave = gerar_chave(segment_count=tamanho, segment_length=segmentos)
        algoritmo = self.cbo_tipo_hash.get() or ALGORITMO_PADRAO
        hash_chave = calcular_hash(chave, algoritmo)

        self._definir_campo(self.txt_key, chave)
        self._definir_campo(self.txt_hash, hash_chave)
        self.btn_gerar.configure(state=tk.NORMAL)
        self._menu_arquivo.entryconfigure(0, state=tk.NORMAL)

    def _copiar(self, texto: str) -> None:
        self.clipboard_clear()
        self.clipboard_append(texto)
        # update() mantém o conteúdo no clipboard mesmo sem eventos de UI.
        self.update()

    def _copiar_chave(self) -> None:
        if self.txt_key.get():
            self._copiar(self.txt_key.get())

    def _copiar_hash(self) -> None:
        if self.txt_hash.get():
            self._copiar(self.txt_hash.get())

    def _salvar(self) -> None:
        if not self.txt_key.get():
            return

        caminho = filedialog.asksaveasfilename(
            title=t("save_file"),
            defaultextension=".txt",
            filetypes=[(t("text_file"), "*.txt"), ("All Files", "*.*")],
        )
        if not caminho:
            return

        conteudo = (
            t("key_line").format(key=self.txt_key.get())
            + "\n"
            + t("hash_line").format(hash=self.txt_hash.get())
            + "\n"
        )
        try:
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write(conteudo)
        except OSError as erro:
            messagebox.showerror(t("error"), t("error_save").format(error=erro))

    def _apoie(self) -> None:
        webbrowser.open(__support_url__)

    def _sobre(self) -> None:
        about = AboutWindow(self)
        about.wait_window()

    def _sair(self) -> None:
        self.destroy()

    def run(self) -> None:
        self.mainloop()
