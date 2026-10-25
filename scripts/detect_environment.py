"""Detecta o ambiente Windows do AURORA 2."""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class EnvironmentReport:
    os_name: str
    os_version: str
    python_version: str
    python_ok: bool
    gpu_name: str
    gpu_ok: bool
    ram_gb: float
    ram_ok: bool
    ollama: bool
    ffmpeg: bool
    git: bool
    github_cli: bool
    aurora_root: str


def command_exists(command: str) -> bool:
    return shutil.which(command) is not None


def detect_gpu() -> tuple[str, bool]:
    nvidia_smi = shutil.which("nvidia-smi")
    if not nvidia_smi:
        return "NVIDIA GPU nao detectada", False
    try:
        result = subprocess.run(
            [nvidia_smi, "--query-gpu=name", "--format=csv,noheader"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        name = result.stdout.strip().splitlines()[0] if result.stdout.strip() else "GPU NVIDIA"
        return name, True
    except (OSError, subprocess.SubprocessError):
        return "GPU NVIDIA detectada, mas nvidia-smi falhou", False


def detect_ram_gb() -> float:
    try:
        result = subprocess.run(
            ["wmic", "ComputerSystem", "get", "TotalPhysicalMemory"],
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        for line in result.stdout.splitlines():
            value = line.strip()
            if value.isdigit():
                return round(int(value) / (1024**3), 2)
    except (OSError, subprocess.SubprocessError):
        pass
    return 0.0


def detect_environment() -> EnvironmentReport:
    aurora_root = Path(os.environ.get("AURORA2_ROOT", Path.home() / "AURORA2"))
    gpu_name, gpu_ok = detect_gpu()
    ram_gb = detect_ram_gb()
    python_version = platform.python_version()
    return EnvironmentReport(
        os_name=platform.system(),
        os_version=platform.version(),
        python_version=python_version,
        python_ok=sys.version_info[:2] == (3, 11),
        gpu_name=gpu_name,
        gpu_ok=gpu_ok,
        ram_gb=ram_gb,
        ram_ok=ram_gb >= 32,
        ollama=command_exists("ollama"),
        ffmpeg=command_exists("ffmpeg"),
        git=command_exists("git"),
        github_cli=command_exists("gh"),
        aurora_root=str(aurora_root),
    )


def main() -> int:
    report = detect_environment()
    for key, value in asdict(report).items():
        print(f"{key}: {value}")
    critical = [report.python_ok, report.ollama, report.ffmpeg, report.git]
    return 0 if all(critical) else 1


if __name__ == "__main__":
    raise SystemExit(main())
