"""Testes do launcher sem abrir o Ardour."""
import os
import stat
import tempfile
import unittest
from pathlib import Path
from aurora2.studio.ardour_launcher import ArdourLauncher

class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.session=self.root/"Teste.ardour"; self.session.write_text("<Session/>",encoding="utf-8")
    def test_validate(self):
        self.assertEqual(ArdourLauncher.validate_session(self.session),self.session.resolve())
    def test_invalid_session(self):
        for value in [self.root/"X.mid",self.root/"X.txt",self.root/"missing.ardour","x.mid"]:
            with self.subTest(value=value),self.assertRaises(ValueError):
                ArdourLauncher.validate_session(value)
    def test_find_executable(self):
        folder=self.root/"Ardour"; folder.mkdir()
        exe=folder/"ardour8.exe"; exe.write_bytes(b"")
        launcher=ArdourLauncher(exe)
        self.assertEqual(launcher.executable,exe)
    def test_missing_executable(self):
        with self.assertRaises(FileNotFoundError):
            ArdourLauncher(self.root/"missing.exe")
    def test_open(self):
        exe=self.root/"fake"; exe.write_text("#!/bin/sh\nexit 0\n",encoding="utf-8")
        exe.chmod(exe.stat().st_mode|stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)
        launcher=ArdourLauncher(exe)
        process=launcher.open(self.session)
        process.wait(timeout=5)
        self.assertEqual(process.args[0],str(exe))
    def test_open_missing_session(self):
        exe=self.root/"fake"; exe.write_text("#!/bin/sh\nexit 0\n",encoding="utf-8")
        exe.chmod(exe.stat().st_mode|stat.S_IXUSR|stat.S_IXGRP|stat.S_IXOTH)
        with self.assertRaises(ValueError):
            ArdourLauncher(exe).open(self.root/"missing.ardour")

if __name__=="__main__":
    unittest.main()
