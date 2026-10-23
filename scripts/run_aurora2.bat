@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%.."
set "PYTHON_EXE=python"

where python >nul 2>nul
if errorlevel 1 (
    echo Python nao encontrado no PATH.
    pause
    exit /b 1
)

if not exist "%PROJECT_ROOT%\.venv" (
    echo Criando ambiente virtual do AURORA 2...
    python -m venv "%PROJECT_ROOT%\.venv"
)

call "%PROJECT_ROOT%\.venv\Scripts\activate.bat"
python -m pip install --upgrade pip >nul
python -m pip install -r "%PROJECT_ROOT%\requirements.txt"

if not exist "%PROJECT_ROOT%\aurora2\__main__.py" (
    echo O nucleo grafico do AURORA 2 ainda nao foi implementado neste estagio.
    echo Ambiente base instalado em: %PROJECT_ROOT%
    pause
    exit /b 0
)

python "%PROJECT_ROOT%\aurora2\__main__.py"
