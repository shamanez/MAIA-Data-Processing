#import face_recognition
import cv2
import numpy as np
import os
import csv
from PIL import Image
import insightface
from pydub import AudioSegment
#from wav2text import wav_conversion

src_dir = './audio/dev/aac/'
tgt_dir = './audio/dev/wav/'
error_csv = './audio_errors.csv'
folder_depth = 3 

audio_all = list()
completed = list()
errors = list()

for r,d,f in os.walk(src_dir):
    for aud in f:
      audio_all.append(os.path.join(r,aud))

for r,d,f in os.walk(tgt_dir):
    for aud in f:
        completed.append('/'.join(os.path.join(r,aud).split('/')[-folder_depth:]))

total = len(audio_all)
count = 0        
for aud in audio_all:
    tgt_filename = aud.split('/')[-1][:-4] + '.wav'
    try:
        tgt_path = os.path.join(tgt_dir,'/'.join(aud.split('/')[-folder_depth:-1]),tgt_filename)
        os.makedirs(os.path.dirname(tgt_path), exist_ok=True)

        sound = AudioSegment.from_file(aud, format="m4a")
        sound = sound.set_channels(1)
        sound = sound.set_frame_rate(16000)
        sound.export(tgt_path, format="wav")
    except:
        errors.append(aud.split('/')[-folder_depth:])
    count += 1
    print(f'{count} of {total}. {round(100*count/total,2)}%. {tgt_filename}')

print(f'Errors: {len(errors)}, {round(100*len(errors)/total,2)}')

with open(error_csv,'a') as fd:
            writer = csv.writer(fd)
            for err in errors:
                writer.writerow(err)