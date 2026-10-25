"""Testes de empacotamento e entrada do AURORA 2."""
import tomllib
import unittest
from pathlib import Path
from aurora2.studio.ardour_cli import build_parser

class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.root=Path(__file__).resolve().parents[1]
    def test_pyproject(self):
        data=tomllib.loads((self.root/"pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(data["project"]["name"],"aurora2")
        self.assertEqual(data["project"]["version"],"0.2.0")
        self.assertEqual(data["project"]["scripts"]["aurora2-studio"],"aurora2.studio.ardour_cli:main")
    def test_cli_entry(self):
        args=build_parser().parse_args(["Balada","tracks.json"])
        self.assertEqual(args.name,"Balada")
        self.assertFalse(args.open)
    def test_version_file(self):
        version=(self.root/"VERSION").read_text(encoding="utf-8").strip().splitlines()[-1]
        self.assertEqual(version,"0.2.0")

if __name__=="__main__":
    unittest.main()
