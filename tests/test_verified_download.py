"""Testes locais sem rede. Execute: python -m unittest discover -s tests -v"""
import hashlib
import io
from pathlib import Path
import tempfile
import unittest
from aurora2.setup.verified_download import acquire, HTTPSOnly

DATA = b"aurora2-tested-content"
SHA = hashlib.sha256(DATA).hexdigest()
URL = "https://example.invalid/file"

class Response(io.BytesIO):
    def geturl(self):
        return URL

class Client:
    def __init__(self, data=DATA):
        self.data = data
        self.calls = 0
    def open(self, url, timeout):
        self.calls += 1
        return Response(self.data)

class VerifiedDownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache = self.root / "cache"
    def test_download(self):
        self.assertEqual(acquire(URL, SHA, self.cache, opener=Client()).read_bytes(), DATA)
    def test_reuse_ai_candidate(self):
        candidate = self.root / "A.I." / "audio acentuado.wav"
        candidate.parent.mkdir()
        candidate.write_bytes(DATA)
        client = Client()
        result = acquire(URL, SHA, self.cache, [candidate], opener=client)
        self.assertEqual(result.read_bytes(), DATA)
        self.assertEqual(candidate.read_bytes(), DATA)
        self.assertEqual(client.calls, 0)
    def test_cache_no_second_download(self):
        client = Client()
        acquire(URL, SHA, self.cache, opener=client)
        acquire(URL, SHA, self.cache, opener=client)
        self.assertEqual(client.calls, 1)
    def test_bad_hash_cleans_partial(self):
        with self.assertRaises(ValueError):
            acquire(URL, SHA, self.cache, opener=Client(b"wrong"))
        self.assertEqual(list(self.cache.iterdir()), [])
    def test_size_limit(self):
        with self.assertRaises(ValueError):
            acquire(URL, SHA, self.cache, max_bytes=2, opener=Client())
        self.assertEqual(list(self.cache.iterdir()), [])
    def test_http_rejected(self):
        with self.assertRaises(ValueError):
            acquire("http://example.invalid/file", SHA, self.cache)
    def test_missing_hash_rejected(self):
        with self.assertRaises(ValueError):
            acquire(URL, "", self.cache)
    def test_corrupt_cache_repaired(self):
        self.cache.mkdir()
        (self.cache / SHA).write_bytes(b"wrong")
        self.assertEqual(acquire(URL, SHA, self.cache, opener=Client()).read_bytes(), DATA)
    def test_downgrade_rejected(self):
        with self.assertRaises(ValueError):
            HTTPSOnly().redirect_request(None, None, 302, "", {}, "http://example.invalid/file")

if __name__ == "__main__":
    unittest.main()
