"""Fluxo completo: cria MIDI, cria sessao Ardour e abre o Ardour."""
from pathlib import Path
from aurora2.studio.ardour_session import create_session
from aurora2.studio.ardour_launcher import ArdourLauncher


def create_and_open(root, name, midi_tracks, bpm=120, ticks_per_beat=480, executable=None, search_paths=()):
    """Cria a sessao e abre o Ardour. Nao controla a interface do programa."""
    if not midi_tracks:
        raise ValueError("O fluxo exige pelo menos uma faixa")
    session_path, midi_path = create_session(root, name, midi_tracks, bpm, ticks_per_beat)
    launcher = ArdourLauncher(executable, search_paths)
    process = launcher.open(session_path)
    return {"session": session_path, "midi": midi_path, "process": process}


def prepare_and_open(root, name, midi_tracks, bpm=120, ticks_per_beat=480, executable=None, search_paths=()):
    """Cria a sessao sem abrir o Ardour; util para testes e revisao."""
    if not midi_tracks:
        raise ValueError("O fluxo exige pelo menos uma faixa")
    session_path, midi_path = create_session(root, name, midi_tracks, bpm, ticks_per_beat)
    ArdourLauncher(executable, search_paths)
    return {"session": session_path, "midi": midi_path}
