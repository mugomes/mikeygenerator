"""Suporte a tradução (en/pt_BR), espelhando os arquivos .po do original."""

from __future__ import annotations

import os

# Texto da licença exibido na janela Sobre (não traduzido no original).
TEXTO_LICENCA = (
    "MiKeyGenerator is free software: you can redistribute it and/or modify it "
    "under the terms of the GNU General Public License as published by the Free "
    "Software Foundation, only version 2 of the License.\n\n"
    "MiKeyGenerator is distributed in the hope that it will be useful, but WITHOUT "
    "ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS "
    "FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details."
)

_STRINGS = {
    "en": {
        "app.title": "MiKeyGenerator",
        "app.description": "Activation key generator.",
        "menu.file": "File",
        "menu.save": "Save",
        "menu.quit": "Quit",
        "menu.about": "About",
        "menu.support": "Support MiKeyGenerator",
        "menu.about_app": "About MiKeyGenerator",
        "menu.theme": "Options",
        "theme.light": "Light",
        "theme.dark": "Dark",
        "hash_type": "Hash Type",
        "segment_size": "Segment Size",
        "key_size": "Key Size",
        "generate": "Generate",
        "generating": "Generating...",
        "activation_key": "Activation Key",
        "hash": "Hash",
        "copy": "Copy",
        "save_file": "Save File",
        "text_file": "Text File",
        "key_line": "Key: {key}",
        "hash_line": "Hash: {hash}",
        "about.title": "About MiKeyGenerator",
        "about.developed_by": "Developed by: Murilo Gomes Julio",
        "about.site": "Site:",
        "about.license": "License: GPL-2.0-only",
        "about.copyright": "Copyright (C) 2024-2026 Murilo Gomes Julio",
        "error": "Error",
        "error_save": "Could not save the file:\n{error}",
    },
    "pt_BR": {
        "app.title": "MiKeyGenerator",
        "app.description": "Gerador de chaves de ativação.",
        "menu.file": "Arquivo",
        "menu.save": "Salvar",
        "menu.quit": "Sair",
        "menu.about": "Sobre",
        "menu.support": "Apoie MiKeyGenerator",
        "menu.about_app": "Sobre MiKeyGenerator",
        "menu.theme": "Opção",
        "theme.light": "Claro",
        "theme.dark": "Escuro",
        "hash_type": "Tipo de Hash",
        "segment_size": "Tamanho do Segmento",
        "key_size": "Tamanho da Chave",
        "generate": "Gerar",
        "generating": "Gerando...",
        "activation_key": "Chave de Ativação",
        "hash": "Hash",
        "copy": "Copiar",
        "save_file": "Salvar arquivo",
        "text_file": "Arquivo de Texto",
        "key_line": "Chave: {key}",
        "hash_line": "Hash: {hash}",
        "about.title": "Sobre MiKeyGenerator",
        "about.developed_by": "Desenvolvido por: Murilo Gomes Julio",
        "about.site": "Site:",
        "about.license": "Licença: GPL-2.0-only",
        "about.copyright": "Copyright (C) 2024-2026 Murilo Gomes Julio",
        "error": "Erro",
        "error_save": "Não foi possível salvar o arquivo:\n{error}",
    },
}

_IDIOMA_ATIVO: str | None = None


def _detectar_idioma() -> str:
    """Retorna o código do idioma a partir das variáveis de ambiente.

    Segue a ordem de precedência habitual do POSIX: LC_ALL, LC_MESSAGES,
    LANGUAGE e LANG. Qualquer código começando com "pt" (ex.: pt_BR,
    pt-PT) seleciona português; caso contrário, usa inglês.
    """
    for var in ("LC_ALL", "LC_MESSAGES", "LANGUAGE", "LANG"):
        valor = os.environ.get(var, "")
        if valor.lower().replace("_", "-").startswith("pt"):
            return "pt_BR"
    return "en"


def t(chave: str) -> str:
    """Retorna a string traduzida para o idioma ativo do sistema."""
    global _IDIOMA_ATIVO
    if _IDIOMA_ATIVO is None:
        _IDIOMA_ATIVO = _detectar_idioma()
    tabela = _STRINGS.get(_IDIOMA_ATIVO, _STRINGS["en"])
    return tabela.get(chave, _STRINGS["en"].get(chave, chave))


def idioma_ativo() -> str:
    """Retorna o código do idioma atualmente selecionado."""
    global _IDIOMA_ATIVO
    if _IDIOMA_ATIVO is None:
        _IDIOMA_ATIVO = _detectar_idioma()
    return _IDIOMA_ATIVO
