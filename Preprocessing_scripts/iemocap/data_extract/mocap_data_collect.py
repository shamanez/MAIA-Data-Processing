import numpy as np
import os
import sys

import wave
import copy
import math

# from keras.models import Sequential, Model
# from keras.layers.core import Dense, Activation
# from keras.layers import LSTM, Input, Flatten, Merge
# from keras.layers.wrappers import TimeDistributed
# from keras.optimizers import SGD, Adam, RMSprop
# from keras.layers.normalization import BatchNormalization
from sklearn.preprocessing import label_binarize


from features import *
from helper import *


batch_size = 64
nb_feat = 34
nb_class = 4
nb_epoch = 80

optimizer = 'Adadelta'


code_path = "/home/gsir059/Documents/PhD/MULTI-MODAL DATASETS/IEMOCAP_full_release"
emotions_used = np.array(['ang', 'exc', 'neu', 'sad'])
data_path = code_path + "/"#../data/sessions/"
sessions = ['Session1', 'Session2', 'Session3', 'Session4', 'Session5']
framerate = 16000

def get_mocap_rot(path_to_mocap_rot, filename, start,end):
    f = open(path_to_mocap_rot + filename, 'r').read()
    f = np.array(f.split('\n'))
    mocap_rot = []
    mocap_rot_avg = []
    f = f[2:]
    counter = 0
    for data in f:
        counter+=1
        data2 = data.split(' ')
        if(len(data2)<2):
            continue
        if(float(data2[1])>start and float(data2[1])<end):
            mocap_rot_avg.append(np.array(data2[2:]).astype(np.float))
            
    mocap_rot_avg = np.array_split(np.array(mocap_rot_avg), 200)
    for spl in mocap_rot_avg:
        mocap_rot.append(np.mean(spl, axis=0))
    return np.array(mocap_rot)

def get_mocap_hand(path_to_mocap_hand, filename, start,end):
    f = open(path_to_mocap_hand + filename, 'r').read()
    f = np.array(f.split('\n'))
    mocap_hand = []
    mocap_hand_avg = []
    f = f[2:]
    counter = 0
    for data in f:
        counter+=1
        data2 = data.split(' ')
        if(len(data2)<2):
            continue
        if(float(data2[1])>start and float(data2[1])<end):
            mocap_hand_avg.append(np.array(data2[2:]).astype(np.float))
            
    mocap_hand_avg = np.array_split(np.array(mocap_hand_avg), 200)
    for spl in mocap_hand_avg:
        mocap_hand.append(np.mean(spl, axis=0))
    return np.array(mocap_hand)

def get_mocap_head(path_to_mocap_head, filename, start,end):
    f = open(path_to_mocap_head + filename, 'r').read()
    f = np.array(f.split('\n'))
    mocap_head = []
    mocap_head_avg = []
    f = f[2:]
    counter = 0
    for data in f:
        counter+=1
        data2 = data.split(' ')
        if(len(data2)<2):
            continue
        if(float(data2[1])>start and float(data2[1])<end):
            mocap_head_avg.append(np.array(data2[2:]).astype(np.float))
            
    mocap_head_avg = np.array_split(np.array(mocap_head_avg), 200)
    for spl in mocap_head_avg:
        mocap_head.append(np.mean(spl, axis=0))
    return np.array(mocap_head)



def read_iemocap_mocap():

    ex_num_a=0
    ex_num_v=0
    ex_num_t=0
    for session in sessions:
        path_to_wav = data_path + session + '/dialog/wav/'
        path_to_emotions = data_path + session + '/dialog/EmoEvaluation/'
        path_to_transcriptions = data_path + session + '/dialog/transcriptions/'
        path_to_vid = data_path + session + '/dialog/avi/DivX/'

     
        files2 = os.listdir(path_to_wav)

      

        files = []
        for f in files2:
            if f.endswith(".wav"):
                if f[0] == '.':
                    files.append(f[2:-4])
                else:
                    files.append(f[:-4])

        for f in files:       
            
            wav = get_audio(path_to_wav, f + '.wav')
            vid_path=get_video(path_to_vid, f + '.mp4')
            transcriptions = get_transcriptions(path_to_transcriptions, f + '.txt')
            emotions = get_emotions(path_to_emotions, f + '.txt')
        
            ex_num_a = split_wav(wav, emotions,ex_num_a)
            ex_num_t=split_text(transcriptions,emotions,ex_num_t)
            ex_num_v = split_avi(vid_path, emotions,ex_num_v)
          
            
    
data = read_iemocap_mocap()

