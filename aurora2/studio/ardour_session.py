"""Criacao de sessao Ardour e importacao de MIDI. Nao abre nem controla o Ardour."""
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET


def safe_name(name):
    if not isinstance(name, str):
        raise ValueError("Nome deve ser texto")
    value = re.sub(r"[^0-9A-Za-z\u00C0-\u024F _-]", "-", name.strip()).strip("-._")
    return value[:80] or "Aurora"


def midi_bytes(midi_tracks, bpm, ticks_per_beat):
    from aurora2.music.midi_writer import build_midi
    return build_midi(midi_tracks, bpm=bpm, ticks_per_beat=ticks_per_beat)


def create_session(root, name, midi_tracks, bpm=120, ticks_per_beat=480):
    """Cria pasta, MIDI e .ardour. Nao executa Ardour nem escreve fora de root."""
    if not isinstance(root, Path):
        root = Path(root)
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Nome da sessao obrigatorio")
    if not midi_tracks or len(midi_tracks) > 64:
        raise ValueError("A sessao exige de 1 a 64 faixas")
    session_name = safe_name(name)
    session = root / session_name
    if session.exists():
        raise FileExistsError(f"Sessao ja existe: {session}")
    session.mkdir(parents=True)
    midi_path = session / f"{session_name}.mid"
    midi_path.write_bytes(midi_bytes(midi_tracks, bpm, ticks_per_beat))
    session_path = session / f"{session_name}.ardour"
    session_path.write_text(render_session(session_name, midi_tracks, bpm), encoding="utf-8")
    metadata = {"name": session_name, "bpm": bpm, "midi": midi_path.name,
                "session": session_path.name, "tracks": len(midi_tracks)}
    (session / "aurora2.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return session_path, midi_path


def render_session(name, midi_tracks, bpm):
    root = ET.Element("Session", {"name": name, "version": "9000",
                                  "id-counter": "1000", "name-counter": "0",
                                  "engine": "PortAudio", "sample-rate": "48000",
                                  "format": "0"})
    ET.SubElement(root, "Config", {"name": "osc-port", "value": "3819"})
    routes = ET.SubElement(root, "Routes")
    for index, track in enumerate(midi_tracks):
        track_name = safe_name(track.get("name", f"Aurora {index + 1}"))
        route = ET.SubElement(routes, "Route", {"id": str(index + 1), "name": track_name,
                                                "type": "MIDI", "active": "1"})
        ET.SubElement(route, "IO", {"inputs": "0", "outputs": "1"})
        ET.SubElement(route, "MIDI", {"channel": str(track.get("channel", 0)),
                                      "program": str(track.get("program", 0))})
        ET.SubElement(route, "Source", {"type": "midi", "file": f"{name}.mid"})
    return ET.tostring(root, encoding="unicode", xml_declaration=True)
