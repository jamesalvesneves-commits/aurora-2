"""Testes UDP reais em loopback; nao substituem teste com Ardour aberto."""
import socket
import struct
import unittest
from aurora2.integrations.ardour_osc import ArdourOSC, encode

class ArdourOSCTests(unittest.TestCase):
    def setUp(self):
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addCleanup(self.receiver.close)
        self.receiver.bind(("127.0.0.1", 0))
        self.receiver.settimeout(2)
        self.client = ArdourOSC(self.receiver.getsockname()[1])
        self.addCleanup(self.client.close)
    def receive(self):
        return self.receiver.recvfrom(65507)[0]
    def test_play_stop(self):
        for action, path in [("play",b"/transport_play\x00"),("stop",b"/transport_stop\x00")]:
            self.client.transport(action)
            self.assertEqual(self.receive(),path+b",\x00\x00\x00")
    def test_mute_solo(self):
        for control in ("mute","solo"):
            self.client.strip(2,control,True)
            packet=self.receive()
            self.assertEqual(packet,encode("/strip/"+control,2,1))
            self.assertTrue(packet.endswith(struct.pack(">ii",2,1)))
    def test_gain(self):
        self.client.strip(1,"volume_db",-12)
        self.assertTrue(self.receive().endswith(struct.pack(">if",1,-12.0)))
    def test_pan(self):
        self.client.strip(3,"pan",0.5)
        self.assertEqual(self.receive(),encode("/strip/pan_stereo_position",3,0.5))
    def test_invalid_controls(self):
        for control,value in [("pan",2),("volume_db",7),("mute",2),("solo",0.5),("pan",True),("pan",float("nan")),("delete",1)]:
            with self.subTest(control=control,value=value), self.assertRaises(ValueError):
                self.client.strip(1,control,value)
    def test_invalid_ids_and_ports(self):
        for ssid in (0,-1,True):
            with self.assertRaises(ValueError):
                self.client.strip(ssid,"mute",1)
        for port in (0,65536,True):
            with self.assertRaises(ValueError):
                ArdourOSC(port)
    def test_codec(self):
        self.assertEqual(encode("/x",2,0.5),b"/x\x00\x00,if\x00"+struct.pack(">if",2,0.5))
        for address,args in [("bad",()),("/x\x00",()),("/x",(float("inf"),))]:
            with self.assertRaises(ValueError):
                encode(address,*args)
    def test_bad_transport(self):
        with self.assertRaises(ValueError):
            self.client.transport("erase")

if __name__ == "__main__":
    unittest.main()
