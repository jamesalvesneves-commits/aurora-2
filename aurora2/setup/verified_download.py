"""Downloads verificados para o novo instalador AURORA 2. Sem execucao de binarios."""
import hashlib
import os
from pathlib import Path
import re
import shutil
import tempfile
import urllib.request
from urllib.parse import urlsplit


def digest(path):
    value = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


class HTTPSOnly(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).scheme.lower() != "https":
            raise ValueError("Redirecionamento sem HTTPS recusado")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def acquire(url, sha256, cache, candidates=(), *, max_bytes=8 * 1024**3, timeout=60, opener=None):
    """Reutiliza candidatos explicitamente fornecidos, incluindo arquivos da pasta A.I.

    O hash deve vir de um manifesto oficial revisado. Nao certifica licencas.
    Retorna um caminho no cache; nunca executa instaladores nem altera candidatos.
    """
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Origem HTTPS sem credenciais obrigatoria")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", sha256):
        raise ValueError("SHA-256 obrigatorio")
    if max_bytes <= 0 or timeout <= 0:
        raise ValueError("Limites invalidos")
    sha256 = sha256.lower()
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / sha256
    if target.is_file() and target.stat().st_size <= max_bytes and digest(target) == sha256:
        return target
    descriptor, name = tempfile.mkstemp(prefix="aurora2-", suffix=".part", dir=cache)
    os.close(descriptor)
    temporary = Path(name)
    try:
        for candidate in map(Path, candidates):
            if candidate.is_file() and candidate.stat().st_size <= max_bytes and digest(candidate) == sha256:
                shutil.copyfile(candidate, temporary)
                break
        else:
            client = opener or urllib.request.build_opener(HTTPSOnly())
            with client.open(url, timeout=timeout) as response, temporary.open("wb") as stream:
                if urlsplit(response.geturl()).scheme.lower() != "https":
                    raise ValueError("Destino sem HTTPS recusado")
                total = 0
                for block in iter(lambda: response.read(1024 * 1024), b""):
                    total += len(block)
                    if total > max_bytes:
                        raise ValueError("Arquivo excede o limite")
                    stream.write(block)
        if temporary.stat().st_size > max_bytes or digest(temporary) != sha256:
            raise ValueError("Integridade invalida")
        os.replace(temporary, target)
        return target
    finally:
        temporary.unlink(missing_ok=True)
