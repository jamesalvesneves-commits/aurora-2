"""Testes da linha de comando sem abrir o Ardour."""
import json
import tempfile
import unittest
from pathlib import Path
from aurora2.studio.ardour_cli import build_parser, load_tracks, main

class CliTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.tracks=[{"name":"Piano","channel":0,"program":0,"notes":[[0,480,62,100]]}]
        self.tracks_path=self.root/"tracks.json"; self.tracks_path.write_text(json.dumps(self.tracks),encoding="utf-8")
        self.exe=self.root/"fake"; self.exe.write_text("#!/bin/sh\nexit 0\n",encoding="utf-8"); self.exe.chmod(0o755)
    def test_parser(self):
        args=build_parser().parse_args(["Balada","tracks.json","--bpm","90","--open"])
        self.assertEqual((args.name,args.bpm,args.open),("Balada",90,True))
    def test_load_tracks(self):
        self.assertEqual(load_tracks(self.tracks_path),self.tracks)
    def test_main_prepare(self):
        code=main(["Balada",str(self.tracks_path),"--root",str(self.root),"--bpm","90","--ardour",str(self.exe)])
        self.assertEqual(code,0)
        self.assertTrue((self.root/"Balada"/"Balada.ardour").is_file())
    def test_main_open(self):
        code=main(["Balada",str(self.tracks_path),"--root",str(self.root),"--bpm","90","--ardour",str(self.exe),"--open"])
        self.assertEqual(code,0)
    def test_invalid_tracks(self):
        bad=self.root/"bad.json"; bad.write_text("{}",encoding="utf-8")
        with self.assertRaises(ValueError): load_tracks(bad)
    def test_missing_executable(self):
        with self.assertRaises(FileNotFoundError): main(["Balada",str(self.tracks_path),"--root",str(self.root),"--ardour",str(self.root/"missing.exe"),"--open"])

if __name__=="__main__":
    unittest.main()
