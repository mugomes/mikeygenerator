"""Lógica pura de geração de chaves e hashes.

Migração do componente gb.hash e da função GerarChave() do projeto
original em Gambas (MiKeyGenerator).

Este módulo não depende de interface gráfica, o que permite testá-lo
de forma isolada.
"""

from __future__ import annotations

import hashlib
import secrets
import string

# Conjunto de caracteres idêntico ao original: a-z, A-Z, 0-9.
CARACTERES = string.ascii_lowercase + string.ascii_uppercase + string.digits

# Algoritmos suportados. O fallback SHA512 preserva o comportamento
# original do "Else" do código Gambas.
ALGORITMOS = ("MD5", "SHA1", "SHA256", "SHA512")
ALGORITMO_PADRAO = "SHA256"
ALGORITMO_FALLBACK = "SHA512"

_HASH_FUNCS = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA512": hashlib.sha512,
}

MINIMO = 1
MAXIMO = 99


def gerar_chave(segment_count: int, segment_length: int) -> str:
    """Gera uma chave de ativação.

    A chave é formada por ``segment_count`` segmentos, cada um com
    ``segment_length`` caracteres aleatórios, unidos por hífen.

    Exemplo (5 segmentos de 5 caracteres): ``x7KpQ-2mNvZ-aBcDe-...``

    Valores inválidos (<= 0) são forçados para o mínimo (1), replicando
    a validação do ``btnGerar_Click`` do projeto original.
    """
    segment_count = max(MINIMO, segment_count)
    segment_length = max(MINIMO, segment_length)

    partes = []
    for _ in range(segment_count):
        parte = "".join(secrets.choice(CARACTERES) for _ in range(segment_length))
        partes.append(parte)
    return "-".join(partes)


def calcular_hash(chave: str, algoritmo: str = ALGORITMO_PADRAO) -> str:
    """Calcula o hash hexadecimal da chave.

    O algoritmo é validado contra uma whitelist. Se o valor informado
    não for reconhecido, usa SHA512 (mesmo fallback do original).
    """
    func = _HASH_FUNCS.get(algoritmo.upper(), _HASH_FUNCS[ALGORITMO_FALLBACK])
    return func(chave.encode("utf-8")).hexdigest()


def ajustar_valor(valor: int) -> int:
    """Garante que o valor esteja dentro dos limites aceitos (1 a 99)."""
    return max(MINIMO, min(MAXIMO, valor))
