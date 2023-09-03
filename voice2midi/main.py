import librosa

from audio_processing.audio_utils import get_dominant_frequency
from audio_processing.midi_utils import MidiNote, generate_midi_file, merge_consecutive_notes, frequency_to_midi

def split_audio(file_path, segment_duration):
    midi_notes = []
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    sample_rate /= 2
    num_segments = int(len(audio_data) / (sample_rate * segment_duration))
    for i in range(num_segments):
        start = int(i * sample_rate * segment_duration)
        end = int((i + 1) * sample_rate * segment_duration)
        segment = audio_data[start:end]
        dominant_frequency = get_dominant_frequency(segment, sample_rate*2)
        midi_note = MidiNote(dominant_frequency, float(start) / sample_rate, float(end) / sample_rate)
        midi_notes.append(midi_note)
    return midi_notes

def main():
    file_path = "audio.wav"
    sample_period = 1.0 / int(input("Introduce los samples por segundo: "))
    midi_notes = split_audio(file_path, sample_period)
    merged_midi_notes = merge_consecutive_notes(midi_notes)
    output_file = "output.mid"
    generate_midi_file(merged_midi_notes, output_file)

if __name__ == "__main__":
    main()
