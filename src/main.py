from drum_synth import DrumSynth
from guitarpro_parser import parse_guitar_pro


if __name__ == "__main__":
    fp = "./data/gp/you-go.gp5"
    hits = parse_guitar_pro(fp)
    drum_synth = DrumSynth()
    drum_synth.play_track(hits, bpm=120)
