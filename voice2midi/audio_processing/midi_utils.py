from midiutil import MIDIFile
import numpy as np

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
    midi_file = MIDIFile(1)
    tempo = 120
    midi_file.addTempo(0, 0, tempo)
    for note in midi_notes:
        track = 0
        channel = 0
        pitch = note.pitch
        start_time = note.start_time
        duration = note.end_time - note.start_time
        velocity = note.velocity
        midi_file.addNote(track, channel, pitch, start_time, duration, velocity)
    with open(output_file, 'wb') as file:
        midi_file.writeFile(file)

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
