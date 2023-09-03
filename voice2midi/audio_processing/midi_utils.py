from midiutil import MIDIFile
import numpy as np


SNAP = True
CLOSE_TO_NOTE_PERCENTAGE = 0.8

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

def frequency_is_close_to_note(notefreq,freq):
    return np.abs(notefreq-freq) <= notefreq * (2 ** (1/12*CLOSE_TO_NOTE_PERCENTAGE) - 1) #Checks difference is less than 3/4 of a semitone (porque podemos)

def merge_consecutive_notes(midi_notes):
    merged_notes = []
    if len(midi_notes) == 0:
        return merged_notes
    current_note = midi_notes[0]
    for i in range(1, len(midi_notes)):
        if midi_notes[i].pitch == current_note.pitch and midi_notes[i].start_time == current_note.end_time:
            current_note.end_time = midi_notes[i].end_time
        else:
            notefreq = midi_to_frequency(current_note.pitch)

            if frequency_is_close_to_note(notefreq, midi_notes[i].frequency) and SNAP:
                current_note.end_time = midi_notes[i].end_time
            else:
                merged_notes.append(current_note)
                current_note = midi_notes[i]
    merged_notes.append(current_note)
    return merged_notes


def remove_noise_notes(merged_midi_notes, min_duration):
    cleaned_notes = []
    prev_note = None

    for note in merged_midi_notes:
        if note.end_time - note.start_time > min_duration:
            # La nota es lo suficientemente larga, la conservamos
            cleaned_notes.append(note)
            prev_note = note
        elif prev_note is not None:
            # Extender la duración de la nota anterior a la eliminada
            prev_note.end_time = note.end_time

    return cleaned_notes


def frequency_to_midi(frequency):
    midi_note = 69 + 12 * np.log2(frequency / 440.0)
    return round(midi_note)

def midi_to_frequency(midi_note):
    frequency = 440.0 * (2 ** ((midi_note - 69) / 12.0))
    return frequency
