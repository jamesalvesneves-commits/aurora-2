"""Testes de sessao Ardour sem abrir o programa."""
import json
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET
from aurora2.studio.ardour_session import create_session, safe_name
from aurora2.music.midi_writer import build_midi

class ArdourSessionTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.tracks=[dict(name="Piano",channel=0,program=0,notes=[(0,480,62,100)]),
                     dict(name="Bateria",channel=9,program=0,notes=[(0,120,36,100)])]
    def test_create(self):
        session,midi=create_session(self.root,"Balada Ré menor",self.tracks,bpm=80)
        self.assertTrue(session.is_file() and midi.is_file())
        self.assertEqual(json.loads((session.parent/"aurora2.json").read_text(encoding="utf-8"))["bpm"],80)
    def test_midi_reusable(self):
        _,midi=create_session(self.root,"Teste",self.tracks)
        self.assertEqual(midi.read_bytes(),build_midi(self.tracks,bpm=120))
    def test_duplicate(self):
        create_session(self.root,"Teste",self.tracks)
        with self.assertRaises(FileExistsError):
            create_session(self.root,"Teste",self.tracks)
    def test_names(self):
        self.assertEqual(safe_name("  Balada/Ré*menor  "),"Balada-Ré-menor")
        self.assertEqual(safe_name("///"),"Aurora")
    def test_session_xml(self):
        session,_=create_session(self.root,"Teste",self.tracks)
        root=ET.fromstring(session.read_text(encoding="utf-8"))
        routes=root.findall("./Routes/Route")
        self.assertEqual([r.attrib["name"] for r in routes],["Piano","Bateria"])
        self.assertEqual(routes[1].attrib["type"],"MIDI")
        self.assertEqual(root.find("./Config").attrib["value"],"3819")
    def test_invalid(self):
        for args in [(self.root,"",self.tracks),(self.root,"x",[]),(self.root,"x",[{}]*65)]:
            with self.subTest(args=args),self.assertRaises(ValueError):
                create_session(*args)
    def test_long_name(self):
        session,_=create_session(self.root,"x"*200,self.tracks)
        self.assertEqual(len(session.stem),80)

if __name__=="__main__":
    unittest.main()
