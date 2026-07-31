#!/usr/bin/env bash
# Build do MiKeyGenerator com PyInstaller (modo onefile).
#
# Uso:
#   ./build.sh
#
# Pré-requisitos: python3. Se o pacote python3-venv não estiver instalado,
# o script usa o fallback com get-pip.py para preparar o ambiente.
set -euo pipefail

cd "$(dirname "$0")"

echo "==> [1/4] Preparando ambiente virtual (venv/)..."
if [ ! -d "venv" ]; then
    if python3 -m venv venv 2>/dev/null; then
        echo "      venv criado com sucesso."
    else
        echo "      ensurepip indisponível; usando fallback com get-pip.py..."
        rm -rf venv
        python3 -m venv --without-pip venv
        curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
        venv/bin/python /tmp/get-pip.py
    fi
fi

echo "==> [2/4] Atualizando pip e instalando dependências..."
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt
venv/bin/pip install -r requirements-dev.txt

echo "==> [3/4] Removendo builds anteriores..."
rm -rf build dist

echo "==> [4/4] Compilando binário único (onefile) -> dist/MiKeyGenerator"
venv/bin/pyinstaller --noconfirm --clean --onefile --name MiKeyGenerator \
    --windowed \
    --add-data "images:images" \
    --collect-data ttkbootstrap \
    --hidden-import PIL._tkinter_finder \
    main.py

echo ""
echo "Build concluído com sucesso!"
echo "  Binário: dist/MiKeyGenerator"
