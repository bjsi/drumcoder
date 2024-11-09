from drum_synth import DrumSynth
from tab_parser import parse_playable_track_from_tab


if __name__ == "__main__":
    fp = "./data/gp/you-go.gp5"
    track = parse_playable_track_from_tab(fp)
    print(track)
    drum_synth = DrumSynth()
    drum_synth.play_track(track)
