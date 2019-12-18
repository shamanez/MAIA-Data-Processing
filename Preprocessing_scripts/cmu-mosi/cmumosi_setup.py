from mmsdk import mmdatasdk 
from tqdm import tqdm
import numpy as np
import os
import zipfile
import requests
import shutil
import csv

# This file downloads csd labels, organises file structure
# Run this file in the parent CMU-MultimodalSDK folder

# Setup folder structure
dst_dir = 'cmu-mosi'
subfolders = ['aligned','csd']  #unzipping creates 'raw' folder
trainfolders = ['train','test','valid']
modfolders = ['audio','video','text']

os.makedirs(dst_dir,exist_ok=True)
for folder in subfolders:
    os.makedirs(os.path.join(dst_dir,folder),exist_ok=True)
for folder in trainfolders:
    os.makedirs(os.path.join(dst_dir,'aligned',folder),exist_ok=True)
    for mod in modfolders:
        os.makedirs(os.path.join(dst_dir,'aligned',folder,mod),exist_ok=True)
print('Folder structure setup complete\nDownloading CSD Labels..')

# Downloads labels into dst dir, create dir if necessary
try:
    cmumosi_labels = mmdatasdk.mmdataset(mmdatasdk.cmu_mosi.labels,os.path.join(dst_dir,'csd'))
    print('CSD labels finished downloading.\nDownloading CMU-MOSI raw data..')
except:
    print('CSD file exists already.\nDownloading CMU-MOSI raw data..')

# Download the CMU-MOSI raw data
url = 'http://immortal.multicomp.cs.cmu.edu/raw_datasets/CMU_MOSI.zip'
filename = url.split('/')[-1]
dl_path = os.path.join(dst_dir,filename)

if not os.path.exists(dl_path):
    r = requests.get(url,stream=True)
    total_size = int(r.headers.get('content-length',0)) / (32*1024)
    block_size = 1024 #1kb
    t = tqdm(total=total_size, unit='B', unit_scale=True)
    with open(dl_path,'wb') as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()

    # Unzip the CMU-MOSI raw data and rename folder to 'raw'
    print('Download complete\nUnzipping raw data..')
    with zipfile.ZipFile(dl_path) as zip_ref:
        zip_ref.extractall(dst_dir)
    os.rename(os.path.join(dst_dir,'Raw'),os.path.join(dst_dir,'raw'))

print('Finished download and folder setup.')

# Load labels into array
dataset = mmdatasdk.mmdataset({0:os.path.join(dst_dir,'csd','CMU_MOSI_Opinion_Labels.csd')})
datadic = dataset.computational_sequences[0].data
files = list()
for key,value in datadic.items():
    files.append(key)

# Get list of standard folders
standard_train_fold=['2iD-tVS8NPw', '8d-gEyoeBzc', 'Qr1Ca94K55A', 'Ci-AH39fi3Y', '8qrpnFRGt2A', 'Bfr499ggo-0', 'QN9ZIUWUXsY', '9T9Hf74oK10', '7JsX8y1ysxY', '1iG0909rllw', 'Oz06ZWiO20M', 'BioHAh1qJAQ', '9c67fiY0wGQ', 'Iu2PFX3z_1s', 'Nzq88NnDkEk', 'Clx4VXItLTE', '9J25DZhivz8', 'Af8D0E4ZXaw', 'TvyZBvOMOTc', 'W8NXH0Djyww', '8OtFthrtaJM', '0h-zjBukYpk', 'Vj1wYRQjB-o', 'GWuJjcEuzt8', 'BI97DNYfe5I', 'PZ-lDQFboO8', '1DmNV9C1hbY', 'OQvJTdtJ2H4', 'I5y0__X72p0', '9qR7uwkblbs', 'G6GlGvlkxAQ', '6_0THN4chvY', 'Njd1F0vZSm4', 'BvYR0L6f2Ig', '03bSnISJMiM', 'Dg_0XKD0Mf4', '5W7Z1C_fDaE', 'VbQk4H8hgr0', 'G-xst2euQUc', 'MLal-t_vJPM', 'BXuRRbG0Ugk', 'LSi-o-IrDMs', 'Jkswaaud0hk', '2WGyTLYerpo', '6Egk_28TtTM', 'Sqr0AcuoNnk', 'POKffnXeBds', '73jzhE8R1TQ', 'OtBXNcAL_lE', 'HEsqda8_d0Q', 'VCslbP0mgZI', 'IumbAb8q2dM']

standard_valid_fold=['WKA5OygbEKI', 'c5xsKMxpXnc', 'atnd_PF-Lbs', 'bvLlb-M3UXU', 'bOL9jKpeJRs', '_dI--eQ6qVU', 'ZAIRrfG22O0', 'X3j2zQgwYgE', 'aiEXnCPZubE', 'ZUXBRvtny7o']

standard_test_fold=['tmZoasNr4rU', 'zhpQhgha_KU', 'lXPQBPVc5Cw', 'iiK8YX8oH1E', 'tStelxIAHjw', 'nzpVDcQ0ywM', 'etzxEpPuc6I', 'cW1FSBF59ik', 'd6hH302o4v8', 'k5Y_838nuGo', 'pLTX3ipuDJI', 'jUzDDGyPkXU', 'f_pcplsH_V0', 'yvsjCA6Y5Fc', 'nbWiPyCm4g0', 'rnaNMUZpvvg', 'wMbj6ajWbic', 'cM3Yna7AavY', 'yDtzw_Y-7RU', 'vyB00TXsimI', 'dq3Nf_lMPnE', 'phBUpBr1hSo', 'd3_k5Xpfmik', 'v0zCBqDeKcE', 'tIrG4oNLFzE', 'fvVhgmXxadc', 'ob23OKe5a9Q', 'cXypl4FnoZo', 'vvZ4IcEtiZc', 'f9O3YtZ2VfI', 'c7UH_rxdZv4']

# Record labels in csv
csv_file_name = 'labels.csv'
csv_header = ['Filename','Start','End','Score','Sentiment','Type'] 
with open(csv_file_name,'w',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(csv_header) 
for f in files:
    for index, (label,time) in enumerate(zip(datadic[f]['features'][:],datadic[f]['intervals'][:]),1):
        filename = f+'_'+str(index)
        start = time.tolist()[0]
        end = time.tolist()[1]
        label = label.tolist()[0]
        sentiment = 'negative' if label < 0 else 'positive'
        folder = 'train'
        if f in standard_valid_fold:
            folder = 'valid'
        elif f in standard_test_fold:
            folder = 'test'
        csv_row = [filename,start,end,label,sentiment,folder]
        csv_row_str = [str(col) for col in csv_row]
        with open(csv_file_name,'a',encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_row_str) 
shutil.move(csv_file_name,os.path.join(dst_dir,'aligned',csv_file_name))
print('Finished recording labels into ', os.path.join(dst_dir,'aligned',csv_file_name))

# Edit vidoes to cut face


# Edit text 

# Organise into folder


audio_dir = os.path.join(dst_dir,'raw','Audio','WAV_16000','Segmented')
video_dir = os.path.join(dst_dir,'raw','Video','Segmented')
text_dir = os.path.join(dst_dir,'raw','Transcript','Segmented') 









