"""Testes do fluxo integrado sem abrir o Ardour."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from aurora2.studio.ardour_workflow import create_and_open, prepare_and_open

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.tracks=[dict(name="Piano",channel=0,program=0,notes=[(0,480,62,100)]),dict(name="Bateria",channel=9,program=0,notes=[(0,120,36,100)])]
        self.exe=self.root/"ardour8.exe"; self.exe.write_bytes(b"")
    def test_prepare(self):
        result=prepare_and_open(self.root,"Balada",self.tracks,bpm=90,executable=self.exe)
        self.assertTrue(result["session"].is_file() and result["midi"].is_file())
    def test_create_and_open(self):
        with patch("aurora2.studio.ardour_launcher.subprocess.Popen") as popen:
            result=create_and_open(self.root,"Balada",self.tracks,bpm=90,executable=self.exe)
        popen.assert_called_once_with([str(self.exe),str(result["session"].resolve())],close_fds=True)
        self.assertEqual(result["process"],popen.return_value)
    def test_empty_tracks(self):
        with self.assertRaises(ValueError): prepare_and_open(self.root,"Vazio",[],executable=self.exe)
    def test_duplicate(self):
        prepare_and_open(self.root,"Balada",self.tracks,executable=self.exe)
        with self.assertRaises(FileExistsError): prepare_and_open(self.root,"Balada",self.tracks,executable=self.exe)
    def test_metadata(self):
        result=prepare_and_open(self.root,"Balada",self.tracks,bpm=90,executable=self.exe)
        meta=json.loads((result["session"].parent/"aurora2.json").read_text(encoding="utf-8"))
        self.assertEqual(meta["bpm"],90)
    def test_missing_executable(self):
        with self.assertRaises(FileNotFoundError): prepare_and_open(self.root,"Balada",self.tracks,executable=self.root/"missing.exe")

if __name__=="__main__":
    unittest.main()
