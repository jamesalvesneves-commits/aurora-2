"""Escritor MIDI padrao, sem dependencias externas. Projeto AURORA 2."""
import math
import struct

MAX_TICK = 0x0FFFFFFF


def integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{name} deve estar entre {low} e {high}")
    return value


def vlq(value):
    integer(value, 0, MAX_TICK, "delta MIDI")
    result = [value & 127]
    value >>= 7
    while value:
        result.insert(0, (value & 127) | 128)
        value >>= 7
    return bytes(result)


def chunk(data):
    return b"MTrk" + struct.pack(">I", len(data)) + data


def build_midi(tracks, bpm=120, ticks_per_beat=480):
    """Retorna Standard MIDI File formato 1.

    Cada faixa: {name, channel, program, notes}.
    Cada nota: (inicio_ticks, duracao_ticks, pitch_0_127, velocity_1_127).
    Canais 0..15; canal 9 e reservado para percussao GM.
    Chamador escolhe o arquivo de destino; esta funcao nao altera disco.
    """
    integer(ticks_per_beat, 1, 32767, "resolucao")
    if isinstance(bpm, bool) or not isinstance(bpm, (int, float)) or not math.isfinite(bpm) or not 20 <= bpm <= 300:
        raise ValueError("BPM deve estar entre 20 e 300")
    tracks = list(tracks)
    integer(len(tracks), 1, 65534, "quantidade de faixas")
    tempo = round(60_000_000 / bpm)
    conductor = b"\x00\xff\x51\x03" + tempo.to_bytes(3, "big")
    conductor += b"\x00\xff\x58\x04\x04\x02\x18\x08\x00\xff\x2f\x00"
    chunks = [chunk(conductor)]
    for track in tracks:
        channel = integer(track.get("channel", 0), 0, 15, "canal")
        program = integer(track.get("program", 0), 0, 127, "instrumento")
        name = track.get("name", "Aurora 2")
        if not isinstance(name, str):
            raise ValueError("Nome da faixa deve ser texto")
        encoded = name.encode("utf-8")
        data = bytearray(b"\x00\xff\x03" + vlq(len(encoded)) + encoded)
        if channel != 9:
            data.extend(bytes((0, 0xC0 | channel, program)))
        events = []
        active = {}
        for note in track.get("notes", ()):
            if len(note) != 4:
                raise ValueError("Nota exige inicio, duracao, pitch e intensidade")
            start, duration, pitch, velocity = note
            integer(start, 0, MAX_TICK, "inicio")
            integer(duration, 1, MAX_TICK, "duracao")
            integer(start + duration, 0, MAX_TICK, "fim")
            integer(pitch, 0, 127, "pitch")
            integer(velocity, 1, 127, "intensidade")
            active.setdefault(pitch, []).append((start, start + duration))
            events.append((start, 1, bytes((0x90 | channel, pitch, velocity))))
            events.append((start + duration, 0, bytes((0x80 | channel, pitch, 0))))
        for intervals in active.values():
            ordered = sorted(intervals)
            if any(current[0] < previous[1] for previous, current in zip(ordered, ordered[1:])):
                raise ValueError("Notas da mesma altura se sobrepoem na faixa")
        previous = 0
        for tick, priority, message in sorted(events):
            data.extend(vlq(tick - previous))
            data.extend(message)
            previous = tick
        data.extend(b"\x00\xff\x2f\x00")
        chunks.append(chunk(bytes(data)))
    header = b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), ticks_per_beat)
    return header + b"".join(chunks)
