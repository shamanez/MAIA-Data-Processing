import os 
import glob
import torch
  

  
def back_translate(folder_path = ".txt"): 

    folder_path = '/home/andrew/voxceleb/final/raw/text_raw'
    tgt_path = '/home/andrew/voxceleb/final/augmented/text_raw'

    for root,dirs,files in os.walk(folder_path):
        eng_files = [os.path.join(root,file) for file in files]

    en2ru = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-ru', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',tokenizer='moses', bpe='fastbpe')

    total = len(eng_files)
    count=0
    
    for file in eng_files:
        if file.endswith('.txt'):

            count+=1
            print(count,round(100*count/total,2),file)

            text_file_source=open(file,'r')
            source_out = text_file_source.readlines()
            final_rus=en2ru.translate(source_out[0])

            folders = file.split('/')
            fold1 = folders[-3]
            fold2 = folders[-2]
            filename = folders[-1]

            path_rus = os.path.join(tgt_path,'rus',fold1,fold2)
            os.makedirs(path_rus,exist_ok=True)
            path_rus = os.path.join(path_rus,filename)

            fh_rus = open(path_rus, "w+") 
            fh_rus.write(final_rus)

    folder_path = os.path.join(tgt_path,'rus')
    for root,dirs,files in os.walk(folder_path):
        rus_files = [os.path.join(root,file) for file in files]

    ru2en = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.ru-en', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',tokenizer='moses', bpe='fastbpe')
    count=0

    for file in rus_files:
        if file.endswith('.txt'):
             
            count+=1
            print(count,round(100*count/total,2),file)

            text_file_source=open(file,'r')
            source_out = text_file_source.readlines()
            final_eng=ru2en.translate(source_out[0])

            folders = file.split('/')
            fold1 = folders[-3]
            fold2 = folders[-2]
            filename = folders[-1]

            path_eng = os.path.join(tgt_path,'rus-eng',fold1,fold2)
            os.makedirs(path_eng,exist_ok=True)
            path_eng = os.path.join(path_eng,filename)

            fh_eng = open(path_eng, "w+") 
            fh_eng.write(final_eng)

if __name__ == '__main__': 
    back_translate()
