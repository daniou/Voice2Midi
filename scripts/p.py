import librosa
import numpy as np
from midiutil import MIDIFile


class MidiNote:
    def __init__(self, frequency, start_time, end_time):
        self.frequency = frequency
        self.pitch = frequency_to_midi(frequency)
        self.start_time = start_time
        self.end_time = end_time
        self.velocity = 100

    def __str__(self):
        return f"Nota MIDI: {self.pitch}, Tiempo de inicio: {self.start_time}, Tiempo de finalización: {self.end_time}, FREQUENCY: {self.frequency}"


def generate_midi_file(midi_notes, output_file):
    # Crear un objeto MIDIFile
    midi_file = MIDIFile(1)  # 1 pista

    # Configurar los parámetros del archivo MIDI
    tempo = 120  # Tempo en BPM
    midi_file.addTempo(0, 0, tempo)

    # Agregar las notas al archivo MIDI
    for note in midi_notes:
        track = 0  # Pista 0
        channel = 0  # Canal 0
        pitch = note.pitch
        start_time = note.start_time
        duration = note.end_time - note.start_time
        velocity = note.velocity

        midi_file.addNote(track, channel, pitch, start_time, duration, velocity)

    # Guardar el archivo MIDI
    with open(output_file, 'wb') as file:
        midi_file.writeFile(file)

def get_dominant_frequency(data, sampling_rate):
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(data))
    peak_coefficient = np.argmax(np.abs(fft_data))
    peak_freq = freqs[peak_coefficient]

    return abs(peak_freq * sampling_rate)


def merge_consecutive_notes(midi_notes):
    merged_notes = []

    if len(midi_notes) == 0:
        return merged_notes

    current_note = midi_notes[0]
    for i in range(1, len(midi_notes)):
        if midi_notes[i].pitch == current_note.pitch and midi_notes[i].start_time == current_note.end_time:
            current_note.end_time = midi_notes[i].end_time
        else:
            merged_notes.append(current_note)
            current_note = midi_notes[i]

    merged_notes.append(current_note)
    return merged_notes


def frequency_to_midi(frequency):
    midi_note = 69 + 12 * np.log2(frequency / 440.0)
    return round(midi_note)


def split_audio(file_path, segment_duration):
    midi_notes = []
    # Cargar el archivo de audio
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    sample_rate /= 2
    # Calcular el número de segmentos
    print(int(len(audio_data) / (sample_rate * segment_duration)))
    num_segments = int(len(audio_data) / (sample_rate * segment_duration))

    # Dividir el archivo de audio en segmentos
    for i in range(num_segments):
        start = int(i * sample_rate * segment_duration)
        end = int((i + 1) * sample_rate * segment_duration)
        print(start, "adasda", end)
        segment = audio_data[start:end]

        dominant_frequency = get_dominant_frequency(segment, sample_rate*2)

        midi_note = MidiNote(dominant_frequency, float(start) / sample_rate, float(end) / sample_rate)
        print(f"Nota midi: {midi_note}")
        midi_notes.append(midi_note)
    return midi_notes

file_path = "audio.wav"
sample_period = 1.0 / int(input("Introduce los samples por segundo: "))
print(sample_period)
midi_notes = split_audio(file_path, sample_period)
merged_midi_notes = merge_consecutive_notes(midi_notes)

output_file = "output.mid"
generate_midi_file(merged_midi_notes, output_file)
