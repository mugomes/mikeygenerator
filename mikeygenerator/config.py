"""Persistência simples de preferências do usuário (JSON).

As configurações são salvas no diretório de configuração do usuário
seguindo o padrão XDG (``$XDG_CONFIG_HOME`` ou ``~/.config``), no
subdiretório ``mikeygenerator/settings.json``.

Para fins de teste/portabilidade, a variável de ambiente
``MIKEY_CONFIG_DIR`` tem prioridade sobre o diretório XDG.
"""

from __future__ import annotations

import json
import os

_NOME_ARQUIVO = "settings.json"


def _diretorio_config() -> str:
    base = (
        os.environ.get("MIKEY_CONFIG_DIR")
        or os.environ.get("XDG_CONFIG_HOME")
        or os.path.join(os.path.expanduser("~"), ".config")
    )
    return os.path.join(base, "mikeygenerator")


def _caminho_config() -> str:
    return os.path.join(_diretorio_config(), _NOME_ARQUIVO)


def carregar() -> dict:
    """Lê as preferências salvas. Retorna um dicionário vazio se não existir."""
    try:
        with open(_caminho_config(), "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
            return dados if isinstance(dados, dict) else {}
    except (OSError, ValueError):
        return {}


def salvar(dados: dict) -> None:
    """Salva as preferências. Falhas de escrita são ignoradas."""
    try:
        os.makedirs(_diretorio_config(), exist_ok=True)
        with open(_caminho_config(), "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    except OSError:
        pass


def obter_tema(padrao: str) -> str:
    """Retorna o tema salvo, ou ``padrao`` se não houver preferência."""
    return carregar().get("tema", padrao)


def salvar_tema(tema: str) -> None:
    """Persiste o tema escolhido sem descartar outras preferências."""
    dados = carregar()
    dados["tema"] = tema
    salvar(dados)
