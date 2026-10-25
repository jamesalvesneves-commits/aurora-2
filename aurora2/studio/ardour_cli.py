"""Linha de comando do AURORA 2 para criar e abrir sessoes Ardour."""
import argparse
import json
from pathlib import Path
from aurora2.studio.ardour_workflow import create_and_open, prepare_and_open


def load_tracks(path):
    tracks = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(tracks, list):
        raise ValueError("O arquivo de faixas deve conter uma lista")
    return tracks


def build_parser():
    parser = argparse.ArgumentParser(prog="aurora2-studio", description="Cria e abre sessoes Ardour")
    parser.add_argument("name", help="Nome da sessao")
    parser.add_argument("tracks", help="Arquivo JSON com as faixas MIDI")
    parser.add_argument("--root", default=".", help="Pasta onde a sessao sera criada")
    parser.add_argument("--bpm", type=int, default=120)
    parser.add_argument("--ticks-per-beat", type=int, default=480)
    parser.add_argument("--ardour", help="Caminho do executavel do Ardour")
    parser.add_argument("--open", action="store_true", help="Abrir o Ardour apos criar a sessao")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    tracks = load_tracks(args.tracks)
    if args.open:
        result = create_and_open(args.root, args.name, tracks, args.bpm, args.ticks_per_beat, args.ardour)
        result.pop("process", None)
    else:
        result = prepare_and_open(args.root, args.name, tracks, args.bpm, args.ticks_per_beat, args.ardour)
    print(json.dumps({"session": str(result["session"]), "midi": str(result["midi"])}, ensure_ascii=False))
    return 0
