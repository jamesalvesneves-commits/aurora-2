"""Instalador idempotente do ambiente base do AURORA 2."""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

from detect_environment import detect_environment

AURORA_FOLDERS = [
    "projects",
    "downloads",
    "models",
    "samples",
    "midi",
    "recordings",
    "stems",
    "exports",
    "logs",
    "scripts",
]

PYTHON_MINIMUM = (3, 11)


def run(command: list[str], check: bool = True) -> subprocess.CompletedProcess:
    print("[AURORA2] Executando:", " ".join(command))
    return subprocess.run(command, check=check, text=True)


def ensure_python() -> None:
    if sys.version_info[:2] < PYTHON_MINIMUM:
        raise SystemExit("AURORA 2 exige Python 3.11 ou superior. Use Python 3.11.9.")
    print(f"[AURORA2] Python {sys.version.split()[0]} detectado.")


def ensure_folders(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    for folder in AURORA_FOLDERS:
        (root / folder).mkdir(parents=True, exist_ok=True)
    print(f"[AURORA2] Estrutura local garantida em: {root}")


def ensure_python_dependencies() -> None:
    requirements = Path(__file__).resolve().parents[1] / "requirements.txt"
    if not requirements.exists():
        raise SystemExit(f"Arquivo nao encontrado: {requirements}")
    run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    run([sys.executable, "-m", "pip", "install", "-r", str(requirements)])


def ensure_external_tool(name: str, command: str, install_hint: str) -> bool:
    if shutil.which(command):
        print(f"[AURORA2] {name} ja esta disponivel.")
        return True
    print(f"[AURORA2] {name} nao encontrado. {install_hint}")
    return False


def download_file(url: str, destination: Path, expected_sha256: str | None = None) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        print(f"[AURORA2] Reutilizando download existente: {destination}")
    else:
        print(f"[AURORA2] Baixando: {url}")
        urllib.request.urlretrieve(url, destination)
    if expected_sha256:
        digest = hashlib.sha256(destination.read_bytes()).hexdigest()
        if digest.lower() != expected_sha256.lower():
            destination.unlink(missing_ok=True)
            raise SystemExit(f"Checksum invalido para {destination.name}.")
        print(f"[AURORA2] Checksum validado: {destination.name}")
    return destination


def create_shortcut(root: Path) -> None:
    desktop = Path(os.environ.get("USERPROFILE", str(Path.home()))) / "Desktop"
    desktop.mkdir(exist_ok=True)
    shortcut = desktop / "AURORA 2.bat"
    launcher = root / "scripts" / "run_aurora2.bat"
    shortcut.write_text(f'@echo off\nstart "" "{launcher}"\n', encoding="utf-8")
    print(f"[AURORA2] Atalho criado: {shortcut}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Instalador base do AURORA 2")
    parser.add_argument(
        "--root",
        default=os.environ.get("AURORA2_ROOT", str(Path.home() / "AURORA2")),
        help="Pasta raiz local do AURORA 2",
    )
    parser.add_argument("--check-only", action="store_true", help="Apenas detectar o ambiente")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    os.environ["AURORA2_ROOT"] = str(root)

    report = detect_environment()
    print("[AURORA2] Ambiente detectado:")
    print(f"  Python: {report.python_version} ({'OK' if report.python_ok else 'INCOMPATIVEL'})")
    print(f"  GPU: {report.gpu_name} ({'OK' if report.gpu_ok else 'NAO DETECTADA'})")
    print(f"  RAM: {report.ram_gb} GB ({'OK' if report.ram_ok else 'ABAIXO DO ALVO'})")
    print(f"  Ollama: {'OK' if report.ollama else 'AUSENTE'}")
    print(f"  FFmpeg: {'OK' if report.ffmpeg else 'AUSENTE'}")
    print(f"  Git: {'OK' if report.git else 'AUSENTE'}")
    print(f"  GitHub CLI: {'OK' if report.github_cli else 'AUSENTE'}")

    if args.check_only:
        return 0

    ensure_python()
    ensure_folders(root)
    ensure_python_dependencies()

    missing = []
    if not ensure_external_tool("Ollama", "ollama", "Instale pelo site oficial e execute 'ollama serve'."):
        missing.append("Ollama")
    if not ensure_external_tool("FFmpeg", "ffmpeg", "Instale FFmpeg e adicione-o ao PATH."):
        missing.append("FFmpeg")
    if not ensure_external_tool("Git", "git", "Instale o Git for Windows."):
        missing.append("Git")
    if not ensure_external_tool("GitHub CLI", "gh", "Instale o GitHub CLI."):
        missing.append("GitHub CLI")

    create_shortcut(root)

    if missing:
        print("[AURORA2] Instalacao base concluida, mas pendencias existem:", ", ".join(missing))
        return 2
    print("[AURORA2] Ambiente base pronto.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
