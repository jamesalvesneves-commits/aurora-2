# Build do executavel Windows do AURORA 2.
$ErrorActionPreference = "Stop"
python -m pip install --upgrade pip
python -m pip install -e . pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --name AURORA2 aurora2/__main__.py
Write-Host "Executavel gerado em dist/AURORA2.exe"
