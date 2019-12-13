import os
import shutil
import csv

# Reorganises files in one folder and records labels in a csv.
src_dir = 'data/'
dst_dir = 'aligned/'
csv_file_name = 'labels.csv'

# Create folders
if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
for folder in ['train','test','valid']:
    if not os.path.exists(os.path.join(dst_dir,folder)):
        os.makedirs(os.path.join(dst_dir,folder))
    for subfolder in ['audio','video','text','AV']:
        if not os.path.exists(os.path.join(dst_dir,folder,subfolder)):
            os.makedirs(os.path.join(dst_dir,folder,subfolder))

# Create .csv file for indexing 
with open(csv_file_name,'w',encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Filename','Modality','neutral','calm','happy','sad','angry','fearful','disgust','surprised'])

# Naming dictionaries
modality= {v:k for v, k in enumerate(['AV','video','audio','text'],1)}
emotion={v:k for v, k in enumerate(['neutral','calm','happy','sad','angry','fearful','disgust','surprised'],1)}
intensity={1:'normal',2:'intense'}
statement={1:'kids',2:'dogs'}

# Walk through src_dir and list all relevant files 
files = list()
for (dirpath, dirnames, filenames) in os.walk(src_dir):
    files += [os.path.join(dirpath, fname) for fname in filenames if fname[-4:] in ['.mp4','.wav']]

# Copy into correct folder and record in .csv 
count=0

for f in files:
    # Slices the files name, removes the file extension
    # splits the string identifiers into an array of ints
    fname = f.rsplit('/',1)[-1][:-4].split('-')
    fname = [int(x) for x in fname]
  
    # Ignore 'song' files
    if fname[1] == 2:
        continue

    # Create descriptive files names
    new_name_arr = [str(i) for i in [emotion[fname[2]],intensity[fname[3]],statement[fname[4]],'actor'+str(fname[6]),fname[5]]]
    new_name = '-'.join(new_name_arr) + f[-4:]
    
    # Copy video to corresponding folder
    subfolder = 'train'
    if fname[6] >= 21:
        subfolder = 'test'
    elif fname[6] >= 23:
        subfolder = 'valid' 
    src = os.path.join(f)
    dst = os.path.join(dst_dir,subfolder,modality[fname[0]],new_name)
    shutil.copy(src,dst)

    # Record file in csv for indexing
    with open(csv_file_name,'a',encoding='utf-8') as file:
        writer = csv.writer(file)
        emotion_arr = [0]*8
        emotion_arr[fname[2]-1] = fname[4]
        csv_arr = [new_name,modality[fname[0]]] + emotion_arr
        csv_arr_str = [str(i) for i in csv_arr]
        writer.writerow(csv_arr_str)
    
    # Progress alert
    count += 1
    percent = round(count / len(files) * 100,2)
    print(f'Preprocessed {f}: {percent}% complete') 

# Remove duplicate lines in csv
#seen = set() # set for fast O(1) amortized lookup
#for line in fileinput.FileInput('1.csv', inplace=1):
#    if line in seen: continue # skip duplicate
#    seen.add(line)
#    print line, # standard output is now redirected to the file

print('Finished aligning data')
     
