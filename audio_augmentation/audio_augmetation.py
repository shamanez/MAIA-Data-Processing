import speech_recognition as sr 
  
import os 
import glob
  
from pydub import AudioSegment 
from pydub.silence import split_on_silence 

import librosa
import numpy as np
import matplotlib.pyplot as plt


class AudioAugmentation:
    def read_audio_file(self, file_path):
        input_length = 16000
        data = librosa.core.load(file_path)[0]
        if len(data) > input_length:
            data = data[:input_length]
        else:
            data = np.pad(data, (0, max(0, input_length - len(data))), "constant")
        return data

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

    def pitch_augment(data, sampling_rate, pitch_factor):
    	return librosa.effects.pitch_shift(data, sampling_rate, pitch_factor)



  

if __name__ == '__main__': 
          
   

    folder_path="./original_audio/"
    
    augmeted_path="./augmeted_audio/"

    aa = AudioAugmentation() #Instance of the class

    for filename in glob.glob(os.path.join(folder_path,'*.wav')):

  
        #opening the .wav file
        #audio = AudioSegment.from_wav(filename) 

        filename=folder_path+filename

        audio = aa.read_audio_file(filename)

        audio_noise = aa.add_noise(audio) #adding the nosie

        audio_roll = aa.shift(audio) #adding the  shifting

        data_stretch = aa.stretch(audio, 0.8) #streching the audio

        data_pitch= aa.pitch_augment(audio, sampling_rate,4)


        aa.plot_time_series(audio)
        aa.plot_time_series(audio_noise)
        aa.plot_time_series(audio_roll)
        aa.plot_time_series(data_stretch)
        aa.plot_time_series(data_pitch)


        aa.write_audio_file(augmeted_path+'noise/'+filename, data_noise)
		aa.write_audio_file(augmeted_path+'roll/'+filename, data_roll)
		aa.write_audio_file(augmeted_path+'stretch/'+filename, data_stretch)
		aa.write_audio_file(augmeted_path+'data_pitch/'+filename, data_pitch)