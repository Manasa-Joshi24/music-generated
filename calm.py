import mido
from mido import MidiFile, MidiTrack, Message, MetaMessage
import random

# Setup
mid = MidiFile(ticks_per_beat=480)
main_track = MidiTrack()
bass_track = MidiTrack()
harmony_track = MidiTrack()
percussion_track = MidiTrack()
mid.tracks.extend([main_track, bass_track, harmony_track, percussion_track])

# Dance tempo
bpm = 128
tempo = mido.bpm2tempo(bpm)
for track in mid.tracks:
    track.append(MetaMessage('set_tempo', tempo=tempo))

# Instruments: Use EDM-like sounds
main_instruments = {'synth_lead': 80, 'square_lead': 81, 'saw_lead': 82}
bass_instruments = {'synth_bass': 38, 'bass_lead': 39}
harmony_instruments = {'pad_1': 88, 'pad_2': 89}
percussion_channel = 9  # Channel 10 in MIDI (starts from 0)

main_instr = random.choice(list(main_instruments.values()))
bass_instr = random.choice(list(bass_instruments.values()))
harmony_instr = random.choice(list(harmony_instruments.values()))

channels = {'main': 0, 'bass': 1, 'harmony': 2, 'percussion': percussion_channel}

# Program change (assign instruments)
main_track.append(Message('program_change', program=main_instr, time=0, channel=channels['main']))
bass_track.append(Message('program_change', program=bass_instr, time=0, channel=channels['bass']))
harmony_track.append(Message('program_change', program=harmony_instr, time=0, channel=channels['harmony']))

# Scale: A minor pentatonic (great for EDM hooks)
scale = [57, 60, 62, 64, 67, 69]  # A C D E G A

def generate_melody(length):
    return [random.choice(scale) for _ in range(length)]

def generate_bass(length):
    return [scale[0] - 12 for _ in range(length)]  # root note in low octave

def generate_harmony(length):
    return [scale[i % len(scale)] + 5 for i in range(length)]  # fifths/pads

def add_notes(track, channel, melody, duration=240, velocity_range=(80, 120)):
    for i, note in enumerate(melody):
        velocity = random.randint(*velocity_range)
        time = 0 if i == 0 else duration
        track.append(Message('note_on', note=note, velocity=velocity, time=time, channel=channel))
        track.append(Message('note_off', note=note, velocity=0, time=duration, channel=channel))

def add_drum_loop(track, bars=16):
    ticks = 480
    kick, snare, hh_closed = 36, 38, 42

    for bar in range(bars):
        for beat in range(4):
            time = ticks if bar > 0 or beat > 0 else 0
            # Kick on every beat
            track.append(Message('note_on', note=kick, velocity=100, time=time, channel=channels['percussion']))
            track.append(Message('note_off', note=kick, velocity=0, time=60, channel=channels['percussion']))

            # Snare on 2 and 4
            if beat in [1, 3]:
                track.append(Message('note_on', note=snare, velocity=80, time=0, channel=channels['percussion']))
                track.append(Message('note_off', note=snare, velocity=0, time=60, channel=channels['percussion']))

            # Hi-hats on off-beats
            track.append(Message('note_on', note=hh_closed, velocity=50, time=60, channel=channels['percussion']))
            track.append(Message('note_off', note=hh_closed, velocity=0, time=60, channel=channels['percussion']))

# Structure
bars = 16
notes_per_bar = 4
total_notes = bars * notes_per_bar

melody = generate_melody(total_notes)
bass = generate_bass(total_notes)
harmony = generate_harmony(total_notes)

add_notes(main_track, channels['main'], melody, duration=240, velocity_range=(100, 127))
add_notes(bass_track, channels['bass'], bass, duration=240, velocity_range=(90, 110))
add_notes(harmony_track, channels['harmony'], harmony, duration=480, velocity_range=(60, 90))
add_drum_loop(percussion_track, 6)

# Save
filename = f"dance_track_{random.randint(1000,9999)}.mid"
mid.save(filename)
print(f"Dance MIDI saved as {filename}")
