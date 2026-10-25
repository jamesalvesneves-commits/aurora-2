"""Testes do launcher sem abrir o Ardour."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from aurora2.studio.ardour_launcher import ArdourLauncher

class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.session=self.root/"Teste.ardour"; self.session.write_text("<Session/>",encoding="utf-8")
        self.exe=self.root/"ardour8.exe"; self.exe.write_bytes(b"")
    def test_validate(self):
        self.assertEqual(ArdourLauncher.validate_session(self.session),self.session.resolve())
    def test_invalid_session(self):
        for value in [self.root/"X.mid",self.root/"X.txt",self.root/"missing.ardour","x.mid"]:
            with self.subTest(value=value),self.assertRaises(ValueError):
                ArdourLauncher.validate_session(value)
    def test_find_executable(self):
        launcher=ArdourLauncher(self.exe)
        self.assertEqual(launcher.executable,self.exe)
    def test_missing_executable(self):
        with self.assertRaises(FileNotFoundError):
            ArdourLauncher(self.root/"missing.exe")
    def test_open(self):
        launcher=ArdourLauncher(self.exe)
        with patch("aurora2.studio.ardour_launcher.subprocess.Popen") as popen:
            process=launcher.open(self.session)
        popen.assert_called_once_with([str(self.exe),str(self.session.resolve())],close_fds=True)
        self.assertEqual(process,popen.return_value)
    def test_open_missing_session(self):
        launcher=ArdourLauncher(self.exe)
        with self.assertRaises(ValueError):
            launcher.open(self.root/"missing.ardour")

if __name__=="__main__":
    unittest.main()
