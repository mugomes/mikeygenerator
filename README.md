# MiKeyGenerator

Gerador de chaves de ativação com cálculo de hash (MD5, SHA1, SHA256, SHA512).

## Funcionalidades

- Geração de chaves no formato `XXXXX-XXXXX-XXXXX-XXXXX-XXXXX`
  (segmentos configuráveis, caracteres `a-z`, `A-Z`, `0-9`)
- Cálculo do hash da chave: MD5, SHA1, SHA256 (padrão) ou SHA512
- Copiar chave ou hash para a área de transferência
- Salvar chave e hash em arquivo de texto (`.txt`)
- Menu "Sobre" com licença GPL-2.0 e link de apoio
- Tradução automática para português do Brasil (via locale do sistema)
- Interface moderna com tema visual **ttkbootstrap**
- Modo escuro (dark mode) via menu **Opção**, com preferência salva

## Requisitos

- Python 3.10 ou superior
- `ttkbootstrap` (tema visual) — dependência de runtime (instalada no venv pelo `build.sh`)
- Para compilar: `curl` disponível. Se o pacote `python3-venv` não estiver
  instalado no sistema, o `build.sh` prepara o ambiente automaticamente
  usando o `get-pip.py` (fallback).

## Execução em desenvolvimento

Após o primeiro `./build.sh` (que cria o venv e instala as dependências):

```bash
venv/bin/python main.py
# ou
venv/bin/python -m mikeygenerator
```

Se preferir usar o Python do sistema, instale a dependência antes:

```bash
python3 -m pip install -r requirements.txt
python3 main.py
```

Para forçar o idioma português:

```bash
LANG=pt_BR.UTF-8 venv/bin/python main.py
```

## Testes

```bash
python3 -m unittest discover -s tests -v
```

## Compilação (PyInstaller)

```bash
./build.sh
```

O script cria o ambiente virtual `venv/`, instala o PyInstaller e gera:

| Modo   | Saída                 |
|--------|-----------------------|
| Único  | `dist/MiKeyGenerator` |

> No Linux, o ícone da janela é definido pelo aplicativo (Tk). Para criar
> um atalho com ícone no menu do sistema, instale um arquivo `.desktop`
> apontando para o executável gerado e para `images/mikeygenerator.png`.

## Autor e Licença

- Autor: Murilo Gomes
- Site: https://profmugomes.com.br

## License

The MiKeyGenerator is provided under:

[SPDX-License-Identifier: GPL-2.0-only](https://spdx.org/licenses/GPL-2.0-only.html)

Beign under the terms of the GNU General Public License version 2 only.

All contributions to the MiKeyGenerator are subject to this license.
