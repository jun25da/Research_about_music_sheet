
import numpy as np
import librosa
from scipy import signal

def BPF(Y,Fs):
    sos = signal.butter(10, [10,11000], 'bp', fs=Fs, output='sos')
    filtd = signal.sosfilt(sos , Y)
    
    return filtd
    

def geomean(plus,minus,freq):
    geo=(plus*minus)**(1/2)
    
    if freq>=geo:
        return plus
    else:
        return minus

def make_frequency_list(onset,y,sr):
    y = BPF(y, sr)
    f, b, c = librosa.pyin( y, fmin=librosa.note_to_hz('C1'),fmax=librosa.note_to_hz('C7'))
    
    
    lengths_f=len(f)
    f=f.tolist()
    #pyin으로 각 프레임의 주파수 추출
    fre=[]
    for i in range(0,len(onset)):
        
        if i==len(onset)-1:
            a=onset[i]
            z=len(f)
            #마지막 음인 경우
        else:
            a=onset[i]
            z=onset[i+1]
        sum=0
        count=0
        for j in range(a,z):
            if str(f[j])=="nan":
                pass
            else:
                sum=sum+f[j]
                count=count+1
        if not count == 0:
            mean=sum/count
            fre.append(mean)
    #length.py에서 얻어진 음길이 정보를 바탕으로 그구간의 평균을 리스트에 저장
    return fre , lengths_f 
            
def make_net_frequency_list(fre,note_12):        
    real_note=[]
    net_note=[]
    for f in range(0,len(fre)):
        note=[] 
        Gap=[0]
        pre=[[0,0],[0,0]]
        breaker=False
        for i in range(1,11):
            for j in range(0,len(note_12)):
                gap=fre[f]-note_12[j][i]
                note.append(note_12[j][i])
                Gap.append(gap)
                pre.append([j,i])
                del pre[0]
                if Gap[-1]*Gap[-2]<0:
                    real=geomean(note[-1],note[-2],fre[f])
                    real_note.append(real)
                    
                    net=f"{note_12[pre[-2][0]][0]}{pre[-2][1]-1}"
                    net_note.append(net)
                    breaker=True
                    break
                
            if breaker==True:
                break
    return net_note


