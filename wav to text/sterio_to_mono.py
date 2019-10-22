import speech_recognition as sr 
  
import os 
import glob
  
from pydub import AudioSegment 
from pydub.silence import split_on_silence 
  
def wav_conversion_mono(folder_path = ".wav"): 


    for filename in glob.glob(os.path.join(folder_path,'*.wav')):

  
        #opening the .wav file
        song = AudioSegment.from_wav(filename) 

        #sterio to mono
        song = song.set_channels(1)
        song = song.set_frame_rate(16000)
        song.export("/home/gsir059/Documents/Aud_Text/mono/"+ filename.split('/')[-1].split(".")[0]+".wav" , format="wav")

    

if __name__ == '__main__': 
          
    print('Enter the sterio audio folder path') 
  
    #folder_path = ".wav/"

    folder_path="/home/gsir059/Documents/Aud_Text/sterio"
    
    

    if not os.path.exists(folder_path):
        exit("not a valid path")
    

  
    wav_conversion_mono(folder_path)