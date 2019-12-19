import csv
import os

def sortTranscript(text_dir,output_dir):
    
    os.makedirs(output_dir,exist_ok=True)

    # Make dictionary of {segment:annotation}
    seg_list = list()
    text_files = os.listdir(text_dir)
    for text_file in text_files:
        with open(os.path.join(text_dir,text_file),'r',encoding='utf-8') as tf:
            for line in tf:
                line_arr = line.split('_')
                segment = text_file.split('.')[0] + '_' + line_arr[0]
                text = ' '.join(line_arr[2].split()).strip()
                seg_list.append([segment,text])
    
    # Create .txt file per segment
    for [segment,text] in seg_list:
        filename = os.path.join(output_dir,segment)
        with open(filename+'.txt', 'w') as file:
            file.write(text)
