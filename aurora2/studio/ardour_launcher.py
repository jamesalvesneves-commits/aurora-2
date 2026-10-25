"""Abertura da sessao Ardour criada pelo AURORA 2. Nao controla a interface."""
import os
import shutil
import subprocess
from pathlib import Path


class ArdourLauncher:
    """Procura o executavel, valida a sessao e abre o Ardour.

    Nao espera nem confirma que a janela abriu; isso exige teste visual no Windows.
    """
    def __init__(self, executable=None, search_paths=()):
        if executable:
            candidates = [Path(executable)]
        else:
            candidates = [Path(p) / name for p in search_paths
                          for name in ("ardour8.exe", "ardour7.exe", "ardour.exe")]
            found = shutil.which("ardour")
            if found:
                candidates.append(Path(found))
        self.executable = next((c for c in candidates if c.is_file()), None)
        if not self.executable:
            raise FileNotFoundError("Executavel do Ardour nao encontrado")

    @staticmethod
    def validate_session(path):
        path = Path(path)
        if not path.is_file() or path.suffix.lower() != ".ardour":
            raise ValueError("Sessao .ardour invalida")
        return path.resolve()

    def open(self, session_path):
        session = self.validate_session(session_path)
        return subprocess.Popen([str(self.executable), str(session)], close_fds=True)
