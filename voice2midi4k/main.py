import librosa
import numpy as np

from voice2midi4k.audio_utils import get_fundamental_frequencies
from voice2midi4k.midi_utils import MidiNote, merge_consecutive_notes, generate_midi_file, remove_noise_notes


def get_midi_notes(data, sr, rms_threshold=0.01):
    fundamental_frequencies = get_fundamental_frequencies(data, sr)
    duration = 2 * len(data) / sr
    midi_notes = []
    if len(fundamental_frequencies) <= 0:
        return midi_notes

    end = 0
    segment_duration = duration / len(fundamental_frequencies)

    for fundamental_frequency in fundamental_frequencies:
        start = end
        end = start + segment_duration
        rms_value = np.sqrt(np.mean(data[int(start * sr / 2):int(end * sr / 2)] ** 2))
        if rms_value >= rms_threshold:
            midi_notes.append(MidiNote(fundamental_frequency, start, end))
    return midi_notes


def postprocess_midi_notes(midi_notes):
    merged_midi_notes = merge_consecutive_notes(midi_notes)
    cleaned_midi_notes = remove_noise_notes(merged_midi_notes, 1.0/20.0)
    final_midi_notes = merge_consecutive_notes(cleaned_midi_notes)
    return final_midi_notes


def audio_to_midi_file(input_path, output_path):
    data, sr = librosa.load(input_path)
    midi_notes = get_midi_notes(data, sr)
    postprocessed_midi_notes = postprocess_midi_notes(midi_notes)
    generate_midi_file(postprocessed_midi_notes, output_path)


def main():
    input_path = "../scripts/audio2.wav"
    output_path = "midi.mid"
    audio_to_midi_file(input_path, output_path)


if __name__ == "__main__":
    main()
