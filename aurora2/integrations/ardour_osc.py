"""Ponte OSC local para Ardour. Envio UDP nao comprova aplicacao do comando."""
import math
import socket
import struct


def osc_string(text):
    raw = text.encode("utf-8") + b"\x00"
    return raw + b"\x00" * (-len(raw) % 4)


def encode(address, *args):
    if not isinstance(address, str) or not address.startswith("/") or "\x00" in address:
        raise ValueError("Endereco OSC invalido")
    tags, body = ",", b""
    for value in args:
        if type(value) is int and -(2**31) <= value < 2**31:
            tags += "i"
            body += struct.pack(">i", value)
        elif type(value) is float and math.isfinite(value):
            tags += "f"
            body += struct.pack(">f", value)
        else:
            raise ValueError("Argumento OSC invalido")
    packet = osc_string(address) + osc_string(tags) + body
    if len(packet) > 65507:
        raise ValueError("Pacote OSC excede limite UDP")
    return packet


class ArdourOSC:
    """Apenas localhost. SSID e a posicao atual da faixa na superficie OSC.

    Requer OSC habilitado no Ardour. Nao gera status conectado a partir de send().
    Port 3819 e padrao do Ardour; porta configuravel para outras instancias.
    """
    def __init__(self, port=3819):
        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError("Porta invalida")
        self.target = ("127.0.0.1", port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.socket.bind(("127.0.0.1", 0))
        except BaseException:
            self.socket.close()
            raise

    def close(self):
        self.socket.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def transport(self, action):
        commands = {"play": "/transport_play", "stop": "/transport_stop",
                    "start": "/goto_start", "panic": "/midi_panic"}
        if action not in commands:
            raise ValueError("Acao de transporte invalida")
        return self.socket.sendto(encode(commands[action]), self.target)

    def strip(self, ssid, control, value):
        if type(ssid) is not int or not 1 <= ssid < 2**31:
            raise ValueError("SSID invalido")
        if control in ("mute", "solo"):
            if type(value) not in (bool, int) or value not in (0, 1):
                raise ValueError("Estado deve ser 0 ou 1")
            argument = int(value)
            path = "/strip/" + control
        else:
            ranges = {"volume_db": (-193, 6, "/strip/gain"),
                      "pan": (0, 1, "/strip/pan_stereo_position")}
            if control not in ranges:
                raise ValueError("Controle invalido")
            low, high, path = ranges[control]
            if type(value) not in (float, int) or not math.isfinite(value) or not low <= value <= high:
                raise ValueError("Valor fora do intervalo")
            argument = float(value)
        return self.socket.sendto(encode(path, ssid, argument), self.target)
