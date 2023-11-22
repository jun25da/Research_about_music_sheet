import librosa
import numpy as np
from itertools import combinations

def analyze_note_lengths(audio_file):
    
    audio, sr = librosa.load(audio_file)

    onsets = librosa.onset.onset_detect(y=audio, sr=sr)
    
    return onsets, audio, sr

def make_lengths_list(onsets, length_f):
    note_lengths = []
    rest_length = []
    for i in range(len(onsets)):
        if i!=len(onsets)-1:
            note_start = onsets[i]
            note_end = onsets[i + 1]
            note_length = note_end - note_start
            #측정한 시간간격을 리스트에 저장
        else:
            note_start=onsets[i]
            note_end=length_f
            note_length = note_end - note_start
            #마지막 음일 경우
            
        note_lengths.append(note_length)
        note_length=note_length.tolist()   
    return note_lengths

        
def analyzing_Tempo(audio, sr):
    beats = librosa.beat.beat_track(y = audio ,sr = sr)
    beat = beats[1]
    first_beat_time, last_beat_time = librosa.frames_to_time((beat[0],beat[-1]), sr = sr)
    Tempo = 60/((last_beat_time-first_beat_time)/(len(beat)-1))
    #이용하여 구현
    return Tempo



def analyzing_beat(note_length,Tempo):
    note_length = np.array(note_length)
    note_length = note_length*(0.093/4)
    note_length = note_length*(Tempo/60)
    
    unique_sums = [0.25, 0.5, 0.75, 1, 1.5, 2.0, 3.0, 4.0]
    for i in range(len(note_length)):
        note_length[i]=decide_beat_length(note_length[i],unique_sums)
    
    note_length = note_length.tolist()
    
    return note_length
    


def decide_beat_length(note,tL): 
    
    for i in range(len(tL)):
        if note <= tL[i]:
            if abs(note-tL[i])>= abs(note-tL[i-1]):
                return tL[i-1]
            else:
                return tL[i]
                

