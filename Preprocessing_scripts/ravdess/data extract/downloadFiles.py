import os
import urllib.request
import zipfile

# Set download destination
dst_dir = 'zip/'
unzip_dir = 'data/'

# Create download destination folder
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
if not os.path.exists(unzip_dir):
    os.makedirs(unzip_dir)

# Create array of url strings to download from
urls = ['https://zenodo.org/record/1188976/files/Audio_Speech_Actors_01-24.zip']
dl_sta = 'https://zenodo.org/record/1188976/files/Video_Speech_Actor_'
dl_end = '.zip'
for i in range(1,25):
    urls += [dl_sta +  "{0:0=2d}".format(i) + dl_end]

# Downloads files and prints progress
count = 0
for url in urls:
    count += 1
    filename = url.split('/')[-1]
    print(f'Downloading {filename}: {count} of {len(urls)}')
    urllib.request.urlretrieve (url, dst_dir+filename)

print('Download complete.')
print('Unzipping files..')

# Unzipping downloaded files into unzip_dir
for item in os.listdir(dst_dir):
    if item.endswith('.zip'):
        zip_dir = os.path.join(dst_dir,item)
        print(f'Unzipping {item}')
        with zipfile.ZipFile(zip_dir) as zip_ref:
            zip_ref.extractall(unzip_dir)
print(f'Unzipped files into {unzip_dir}')

