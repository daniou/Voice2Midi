import librosa
import numpy as np
import soundfile as sf
from audio_processing.audio_utils import get_dominant_frequency
from audio_processing.midi_utils import MidiNote, generate_midi_file, merge_consecutive_notes, frequency_to_midi, \
    remove_noise_notes


def split_audio(file_path, segment_duration, rms_threshold=0.01):
    midi_notes = []
    audio_data, sample_rate = librosa.load(file_path)
    sample_rate /= 2
    num_segments = int(len(audio_data) / (sample_rate * segment_duration))
    for i in range(num_segments):
        start = int(i * sample_rate * segment_duration)
        end = int((i + 1) * sample_rate * segment_duration)
        segment = audio_data[start:end]

        # Calcular el valor RMS del segmento
        rms_value = np.sqrt(np.mean(segment ** 2))

        if rms_value >= rms_threshold:
            dominant_frequency = get_dominant_frequency(segment, sample_rate * 2)
            if dominant_frequency  > 1:
                midi_note = MidiNote(dominant_frequency, float(start) / sample_rate, float(end) / sample_rate)
                print(midi_note)
                midi_notes.append(midi_note)
        else:
            print("silencio")
    return midi_notes


def print_freqs(midi_notes):
    for note in midi_notes:
        print(note.frequency)



def main():
    file_path = "../scripts/audio2.wav"
    sample_period = 1.0 / 20#int(input("Introduce los samples por segundo: "))
    midi_notes = split_audio(file_path, sample_period)
    print_freqs(midi_notes)
    merged_midi_notes = merge_consecutive_notes(midi_notes)
    cleaned_midi_notes = merged_midi_notes#remove_noise_notes(merged_midi_notes, sample_period*2)
    final_midi_notes = merge_consecutive_notes(cleaned_midi_notes)
    output_file = "output3.mid"
    generate_midi_file(final_midi_notes, output_file)

if __name__ == "__main__":
    main()
