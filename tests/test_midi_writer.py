"""Testes do escritor MIDI real, sem DAW ou rede."""
import struct
import unittest
from aurora2.music.midi_writer import build_midi, vlq

class MidiWriterTests(unittest.TestCase):
    def track(self, notes=None, **kw):
        return dict(name="Piano", notes=notes if notes is not None else [(0, 480, 62, 100)], **kw)
    def test_header_and_track_lengths(self):
        data = build_midi([self.track()])
        self.assertEqual(struct.unpack(">4sIHHH", data[:14]), (b"MThd", 6, 1, 2, 480))
        position = 14
        for _ in range(2):
            self.assertEqual(data[position:position+4], b"MTrk")
            length = struct.unpack(">I", data[position+4:position+8])[0]
            body = data[position+8:position+8+length]
            self.assertTrue(body.endswith(b"\x00\xff\x2f\x00"))
            position += 8 + length
        self.assertEqual(position, len(data))
    def test_tempo(self):
        self.assertIn(b"\xff\x51\x03" + (750000).to_bytes(3,"big"), build_midi([self.track()], bpm=80))
    def test_note_duration(self):
        self.assertIn(b"\x00\x90\x3e\x64\x83\x60\x80\x3e\x00", build_midi([self.track()]))
    def test_drums(self):
        data = build_midi([self.track(channel=9)])
        self.assertIn(b"\x99\x3e\x64", data)
        self.assertNotIn(b"\xc9", data)
    def test_vlq(self):
        self.assertEqual(vlq(0), b"\x00")
        self.assertEqual(vlq(127), b"\x7f")
        self.assertEqual(vlq(128), b"\x81\x00")
        self.assertEqual(vlq(0x0FFFFFFF), b"\xff\xff\xff\x7f")
    def test_invalid_notes(self):
        for note in [(-1,480,60,100),(0,0,60,100),(0,480,128,100),(0,480,60,0),(0,480,True,100)]:
            with self.subTest(note=note), self.assertRaises(ValueError):
                build_midi([self.track([note])])
    def test_invalid_tempo(self):
        for bpm in [0,301,float("nan"),True]:
            with self.subTest(bpm=bpm), self.assertRaises(ValueError):
                build_midi([self.track()],bpm=bpm)
    def test_overlap_rejected(self):
        with self.assertRaises(ValueError):
            build_midi([self.track([(0,480,60,90),(240,480,60,90)])])
    def test_adjacent_notes(self):
        data = build_midi([self.track([(0,480,60,90),(480,480,60,90)])])
        self.assertIn(b"\x80\x3c\x00\x00\x90\x3c\x5a", data)
    def test_multiple_tracks(self):
        data = build_midi([self.track(), self.track(channel=1,program=32)])
        self.assertEqual(struct.unpack(">H",data[10:12])[0],3)
    def test_utf8_name(self):
        self.assertIn("Percussao — Aurora".encode(),build_midi([dict(name="Percussao — Aurora",notes=[])]))

if __name__ == "__main__":
    unittest.main()
