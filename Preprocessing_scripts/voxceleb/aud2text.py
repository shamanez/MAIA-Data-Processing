import numpy as np
import os
import io
import csv
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import speech_v1p1beta1
import random

src_dir = './audio/dev/wav/'
tgt_dir = './text/'
result_csv = './aud2text_results.csv'
shuffled_list = './aud2text_shuffled.csv'
folder_depth = 3 
record_freq = 50 

audio_all = list()
completed = list()
results = list()

# for r, d, f in os.walk(src_dir):
#     for aud in f:
#         audio_all.append(os.path.join(r, aud))

# for r, d, f in os.walk(tgt_dir):
#     for aud in f:
#         completed.append(
#             '/'.join(os.path.join(r, aud).split('/')[-folder_depth:]))

# Create shuffled order
# random.Random(1).shuffle(audio_all)
# total = len(audio_all)
# count = 0
# with open(shuffled_list, 'a') as fd:
#     writer = csv.writer(fd)
#     for aud in audio_all:
#         count += 1
#         print(round(100*count/total,3))
#         writer.writerow([aud])

with open(shuffled_list) as shuffled:
    readCSV = csv.reader(shuffled, delimiter=',')
    for aud in readCSV:
        audio_all += aud 

# Load client
client1 = speech_v1p1beta1.SpeechClient()
# client2 = speech.SpeechClient()

# Setup Config
config1 = {
    "language_code": 'en',
    "alternative_language_codes": ['hi', 'fr', 'de'],
}
# config2 = types.RecognitionConfig(
#     encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=16000,
#     language_code='en-US',
#     model='video'
# )

_total = len(audio_all)
total = 50000 
count = 0
errors = 0
non_english = 0

for aud in audio_all:
    if count >= total:
        break
    
    tgt_savename = '/'.join(aud.split('/')[-folder_depth:])[:-4]
    language = 'error'
    confidence1 = 0
    confidence2 = 0

    try:
        # Loads the audio into memory
        with io.open(aud, "rb") as f:
            content = f.read()
        audio1 = {"content": content}
        # audio2 = types.RecognitionAudio(content=content)

        # Detect 1
        response1 = client1.recognize(config1, audio1)
        for res in response1.results:
            language = res.language_code
            rec1 = res.alternatives[0].transcript
            confidence1 = res.alternatives[0].confidence

        # Ignore non-english
        if language[:2] != 'en':
            results.append([tgt_savename, language, confidence1])
            non_english += 1
            count += 1 
            print(f'{round(100*count/total,3)}%. {count} of {total}. foreign: {non_english}, errors: {errors}. {tgt_savename}')
            continue

        # # Detect 2
        # response2 = client2.recognize(config2, audio2)
        # for res in response2.results:
        #     rec2 = res.alternatives[0].transcript
        #     confidence2 = res.alternatives[0].confidence

        # Record results
        tgt_dir = tgt_dir
        tgt_folder = '/'.join(aud.split('/')[-folder_depth:-1])
        tgt_filename = os.path.basename(aud)[:-4] + '.txt'
        tgt_path = os.path.join(tgt_dir, tgt_folder, tgt_filename)
        os.makedirs(os.path.dirname(tgt_path), exist_ok=True)
        fh = open(tgt_path, "w+")
        transcript = rec2 if confidence2 > confidence1 else rec1
        fh.write(transcript + ".")

        confidence2 = 0
        rec2 = None
        results.append([tgt_savename, 'en', confidence1,confidence2, rec1, rec2])

    except:
        errors += 1
        results.append([tgt_savename, language, 0,0])

    # Staggered logs
    count += 1
    if count % record_freq == 0 or count >= total:
        with open(result_csv, 'a') as fd:
            writer = csv.writer(fd)
            for result in results:
                writer.writerow(result)
        results = list()
    print(f'{round(100*count/total,3)}%. {count} of {total}. foreign: {non_english}. errors: {errors}. {tgt_savename}')