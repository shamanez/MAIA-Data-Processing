import shutil
import os
import csv
src = './audio/dev/wav/'
dst = './final/audio_raw'
count=0
with open('summary_85plus.csv','r') as inp:
    for row in csv.reader(inp):
        if row[0] == "File":
            continue
        path = os.path.join(dst,row[1],row[2])
        os.makedirs(path,exist_ok=True)
        vid = os.path.join(src,row[1],row[2],row[3]+'.wav')
        shutil.copy(vid,os.path.join(path,row[3]+'.wav'))
        count += 1
        print(count,path,vid)
