@echo off

if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    python -m venv .venv
)

call .venv\Scripts\activate

echo Instalando dependencias...
python -m pip install -r requirements.txt

echo.
echo Iniciando Biblioteca...
echo.

python main.py

pause