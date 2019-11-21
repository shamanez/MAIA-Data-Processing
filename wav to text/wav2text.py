import speech_recognition as sr 
  
import os 
import glob
  
from pydub import AudioSegment 
from pydub.silence import split_on_silence 

import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

  
def wav_conversion(folder_path = ".wav"): 

    client = speech.SpeechClient()
    corrupted_aud="/home/gsir059/Documents/Aud_Text/corrupted_ex.txt"
    corrupted_log = open(corrupted_aud, "w+") 


    for filename in glob.glob(os.path.join(folder_path,'*.wav')):

  
        #opening the .wav file
        #song = AudioSegment.from_wav(filename) 


        text_file_name="/home/gsir059/Documents/Aud_Text/text/"+ filename.split('/')[-1].split(".")[0] + '.txt'
        
       
        # #write the recognized text  
        fh = open(text_file_name, "w+") 

        #r = sr.Recognizer()

        try: 
            # Loads the audio into memory
            with io.open(filename, 'rb') as audio_file:
                content = audio_file.read()
                audio = types.RecognitionAudio(content=content)

            config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US',
            model='video')


            response = client.recognize(config, audio)

            
            for result in response.results:
                print(result)
                rec=result.alternatives[0].transcript
                fh.write(rec+". ")

       
            # with sr.AudioFile(filename) as source:
            #         audio = r.record(source)  # read the entire audio file   
            #         rec=r.recognize_google(audio)               
            #         fh.write(rec+". ") 
                   

        # catch any errors.  except sr.UnknownValueError:
        except sr.UnknownValueError: 
            corrupted_log.write(filename+'\n') 
            print("Could not understand audio") 

        except sr.RequestError as e: 
            print("Could not request results. check your internet connection") 

    

if __name__ == '__main__': 
          
    print('Enter the audio folder path') 
  
    #folder_path = ".wav/"

    folder_path="/home/gsir059/Documents/Aud_Text/mono"
    
    

    if not os.path.exists(folder_path):
        exit("not a valid path")
    

  	
    wav_conversion(folder_path)