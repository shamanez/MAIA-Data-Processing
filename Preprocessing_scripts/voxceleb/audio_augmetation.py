import speech_recognition as sr 
  
import os 
import glob
import random  
from pydub import AudioSegment 
from pydub.silence import split_on_silence 

import librosa
import numpy as np
import matplotlib.pyplot as plt


class AudioAugmentation:
    def read_audio_file(self, file_path):
        input_length = 16000
        data,sr = librosa.core.load(file_path)
        if len(data) < input_length:
            data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
        return data,sr

    def write_audio_file(self, file, data, sample_rate=16000):
        librosa.output.write_wav(file, data, sample_rate)

    def plot_time_series(self, data):
        fig = plt.figure(figsize=(14, 8))
        plt.title('Raw wave ')
        plt.ylabel('Amplitude')
        plt.plot(np.linspace(0, 1, len(data)), data)
        plt.show()

    def add_noise(self, data):
        noise = np.random.randn(len(data))
        data_noise = data + 0.005 * noise
        return data_noise

    def shift(self, data):
        return np.roll(data, 1600)

    def stretch(self, data, rate=1):
        input_length = 16000
        data = librosa.effects.time_stretch(data, rate)
        if len(data) > input_length:
            data = data[:input_length]
        else:
            data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
        return data

    def pitch_augment(self,data, sampling_rate, pitch_factor):
    	return librosa.effects.pitch_shift(data, sampling_rate, n_steps=pitch_factor)



  

if __name__ == '__main__': 
          
    folder_path="./final/raw/audio_raw/"
    augmented_path="./final/augmented/audio/"
    
    aa = AudioAugmentation() #Instance of the class
    count = 0
    for root, dirs, files in os.walk(folder_path): 
        for file in files:
            count += 1
            print(count,file)
            if file.endswith('.wav'):
                filename=os.path.join(root,file)  
                folders = filename.split('/')
                fold1 = folders[-3]
                fold2 = folders[-2]

                audio, sampling_rate = aa.read_audio_file(filename)
                audio_noise = aa.add_noise(audio) #adding the nosie
                audio_roll = aa.shift(audio) #adding the  shifting
                data_stretch = aa.stretch(audio, 0.8) #streching the audio
                data_pitch= aa.pitch_augment(audio,sampling_rate,random.randint(-5,5))

                # aa.plot_time_series(audio)
                # aa.plot_time_series(audio_noise)
                # aa.plot_time_series(audio_roll)
                # aa.plot_time_series(data_stretch)
                # aa.plot_time_series(data_pitch)
                for name in ['noise','roll','stretch','data_pitch']:
                    path = os.path.join(augmented_path,name,fold1,fold2)
                    os.makedirs(path,exist_ok=True)
                    
                aa.write_audio_file(os.path.join(augmented_path,'noise',fold1,fold2,file), audio_noise, sampling_rate)
                aa.write_audio_file(os.path.join(augmented_path,'roll',fold1,fold2,file), audio_roll, sampling_rate)
                aa.write_audio_file(os.path.join(augmented_path,'stretch',fold1,fold2,file), data_stretch, sampling_rate)
                aa.write_audio_file(os.path.join(augmented_path,'data_pitch',fold1,fold2,file), data_pitch, sampling_rate)
