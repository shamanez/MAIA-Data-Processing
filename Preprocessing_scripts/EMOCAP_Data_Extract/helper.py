import os
import csv
import wave
import sys
import numpy as np
import pandas as pd
import glob
import array
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip



EMOTION_ENCODING = {'ang': 0, 'exc': 1,'fru':2,'neu':3,'sad': 4, 'sur': 5,'hap':6,'xxx':7}

from pydub import AudioSegment
import librosa

def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def split_avi(avi_name, emotions,ex):

    emotions_used = np.array(['ang', 'exc','fru','sad', 'neu', 'sur','hap'])


    for ie, e in enumerate(emotions):
          
            label=e['emotion']

            if not label in emotions_used:
                continue
            filename=str(ex)+"_"+label +".mp4"


            start = e['start']
            end = e['end']
         

            with open('/home/gsir059/Desktop/Raw_Data/labels_train_v.txt', 'a') as label_file:
                text =  filename + '\t' + str(EMOTION_ENCODING[label]) + '\n'
                label_file.write(text)
            
            targetname='/home/gsir059/Desktop/Raw_Data/Video/'+filename

          
            with VideoFileClip(avi_name) as video:
                if video.duration < end:
                    end= video.duration
                new = video.subclip(start, end)
                new.write_videofile(targetname, audio_codec='aac')

            ex=ex+1

    return ex


def split_wav(wav, emotions,ex):
    (nchannels, sampwidth, framerate, nframes, comptype, compname), samples = wav

    left = samples[0::nchannels]
    right = samples[1::nchannels]
    emotions_used = np.array(['ang', 'exc','fru','sad', 'neu', 'sur','hap'])

    frames = []
    for ie, e in enumerate(emotions):
        label=e['emotion']

        if not label in emotions_used:
            continue
        filename=str(ex)+"_"+label +".wav"


        start = e['start']
        end = e['end']

        e['right'] = right[int(start * framerate):int(end * framerate)]
        e['left'] = left[int(start * framerate):int(end * framerate)]

        array_type = {1:'B', 2: 'h', 4: 'l'}[sampwidth]


        

        with open('/home/gsir059/Desktop/Raw_Data/labels_train_a.txt', 'a') as label_file:
            text =  filename + '\t' + str(EMOTION_ENCODING[label]) + '\n'
            label_file.write(text)
        

            
        audio_chunk = array.array(array_type, e['left'].tobytes())
        ofile = wave.open('/home/gsir059/Desktop/Raw_Data/Audio/'+filename, 'w')
        ofile.setparams((1, sampwidth, framerate, len(e['left']), comptype, compname))
        ofile.writeframes(audio_chunk.tostring())
        ofile.close()
    
        ex=ex+1
    return ex

def split_text(txt, emotions,ex):
    

    emotions_used = np.array(['ang', 'exc','fru','sad', 'neu', 'sur','hap'])

   
    for ie, e in enumerate(emotions):
            label=e['emotion']

            if not label in emotions_used:
                continue
            filename=str(ex)+"_"+label +".txt"

            real_text= txt[e['id']]
            
           

            with open('/home/gsir059/Desktop/Raw_Data/labels_train_t.txt', 'a') as label_file:
                text =  filename + '\t' + str(EMOTION_ENCODING[label]) + '\n'
                label_file.write(text)

            with open('/home/gsir059/Desktop/Raw_Data/Text/'+filename, 'a') as source_file:
                #text =  filename + '\t' + str(EMOTION_ENCODING[label]) + '\n'
                source_file.write(real_text)
          
            ex=ex+1
           
   
    return ex



def get_field(data, key):
    return np.array([e[key] for e in data])

def pad_sequence_into_array(Xs, maxlen=None, truncating='post', padding='post', value=0.):

    Nsamples = len(Xs)
    if maxlen is None:
        lengths = [s.shape[0] for s in Xs]    # 'sequences' must be list, 's' must be numpy array, len(s) return the first dimension of s
        maxlen = np.max(lengths)

    Xout = np.ones(shape=[Nsamples, maxlen] + list(Xs[0].shape[1:]), dtype=Xs[0].dtype) * np.asarray(value, dtype=Xs[0].dtype)
    Mask = np.zeros(shape=[Nsamples, maxlen], dtype=Xout.dtype)
    for i in range(Nsamples):
        x = Xs[i]
        if truncating == 'pre':
            trunc = x[-maxlen:]
        elif truncating == 'post':
            trunc = x[:maxlen]
        else:
            raise ValueError("Truncating type '%s' not understood" % truncating)
        if padding == 'post':
            Xout[i, :len(trunc)] = trunc
            Mask[i, :len(trunc)] = 1
        elif padding == 'pre':
            Xout[i, -len(trunc):] = trunc
            Mask[i, -len(trunc):] = 1
        else:
            raise ValueError("Padding type '%s' not understood" % padding)
    return Xout, Mask


def convert_gt_from_array_to_list(gt_batch, gt_batch_mask=None):

    B, L = gt_batch.shape
    gt_batch = gt_batch.astype('int')
    gts = []
    for i in range(B):
        if gt_batch_mask is None:
            l = L
        else:
            l = int(gt_batch_mask[i, :].sum())
        gts.append(gt_batch[i, :l].tolist())
    return gts

def get_audio(path_to_wav, filename):
    wav = wave.open(path_to_wav + filename, mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    content = wav.readframes(nframes)
    samples = np.fromstring(content, dtype=np.int16)
    return (nchannels, sampwidth, framerate, nframes, comptype, compname), samples

def get_video(path_to_vid, filename):

    path=path_to_vid+filename
  
    return path


def get_transcriptions(path_to_transcriptions, filename):
    f = open(path_to_transcriptions + filename, 'r').read()
    f = np.array(f.split('\n'))
    transcription = {}
    for i in range(len(f) - 1):
        g = f[i]
        i1 = g.find(': ')
        i0 = g.find(' [')
        ind_id = g[:i0]
        ind_ts = g[i1+2:]
        transcription[ind_id] = ind_ts
    return transcription


def get_emotions(path_to_emotions, filename):
    f = open(path_to_emotions + filename, 'r').read()
    f = np.array(f.split('\n'))
    idx = f == ''
    idx_n = np.arange(len(f))[idx]
    emotion = []
    for i in range(len(idx_n) - 2):
        g = f[idx_n[i]+1:idx_n[i+1]]
        head = g[0]
        i0 = head.find(' - ')
        start_time = float(head[head.find('[') + 1:head.find(' - ')])
        end_time = float(head[head.find(' - ') + 3:head.find(']')])
        actor_id = head[head.find(filename[:-4]) + len(filename[:-4]) + 1:
                        head.find(filename[:-4]) + len(filename[:-4]) + 5]
        emo = head[head.find('\t[') - 3:head.find('\t[')]
        vad = head[head.find('\t[') + 1:]

        v = float(vad[1:7])
        a = float(vad[9:15])
        d = float(vad[17:23])
        
        j = 1
        emos = []
        while g[j][0] == "C":
            head = g[j]
            start_idx = head.find("\t") + 1
            evoluator_emo = []
            idx = head.find(";", start_idx)
            while idx != -1:
                evoluator_emo.append(head[start_idx:idx].strip().lower()[:3])
                start_idx = idx + 1
                idx = head.find(";", start_idx)
            emos.append(evoluator_emo)
            j += 1

        emotion.append({'start': start_time,
                        'end': end_time,
                        'id': filename[:-4] + '_' + actor_id,
                        'v': v,
                        'a': a,
                        'd': d,
                        'emotion': emo,
                        'emo_evo': emos})
    return emotion