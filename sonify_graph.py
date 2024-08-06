from gensound import WAV, test_wav, Sine, Triangle, Square, Pan

sig = Triangle 

beat = 0.5e3 # 120 bpm
fermata = 0.1 
pause = 0.6 


def transform_notes(music: list):
    sol = []
    input_range = max(music)
    output_range = 48
    scale = output_range/input_range

    for i in range(len(music)):
        sol.append(music[i] * scale)
    
    return sol


def create_melody(notes):
    note_names = [
        "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2", "A2", "A#2", "B2",
        "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3", "A3", "A#3", "B3",
        "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4", "A4", "A#4", "B4",
        "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5", "A5", "A#5", "B5",
        "C6"
    ]
    
    melody = []
    for note in notes:
        index = round(note)
        if 0 <= index < len(note_names):
            melody.append(f"{note_names[index]}=0.50")
        else:
            raise ValueError(f"Input value {note} is out of range (0-48)")
    
    return " ".join(melody)
