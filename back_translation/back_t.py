
import os 
import glob

import torch
  

  
def back_translate(folder_path = ".txt"): 
    en2de = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-de', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                       tokenizer='moses', bpe='fastbpe')


    de2en = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.de-en', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                        tokenizer='moses', bpe='fastbpe')

 
    en2ru = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.en-ru', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                        tokenizer='moses', bpe='fastbpe')

    ru2en = torch.hub.load('pytorch/fairseq', 'transformer.wmt19.ru-en', checkpoint_file='model1.pt:model2.pt:model3.pt:model4.pt',
                        tokenizer='moses', bpe='fastbpe')

    for filename in glob.glob(os.path.join(folder_path,'*.txt')):

  
        text_file_name="/home/gsir059/Documents/Aud_Text/text/"+ filename.split('/')[-1].split(".")[0] + '.txt'
        text_file_name_new="/home/gsir059/Documents/Aud_Text/text_new/"+ filename.split('/')[-1].split(".")[0] + '.txt'
        text_file_name_new_rus="/home/gsir059/Documents/Aud_Text/text_new_rus/"+ filename.split('/')[-1].split(".")[0] + '.txt'
        
        text_file_source=open(text_file_name,'r')
        source_out = text_file_source.readlines()


        
        german_text=en2de.translate(source_out[0])
        rus_text=en2ru.translate(source_out[0])
        final_english=de2en.translate(german_text)
        final_rus=ru2en.translate(rus_text)

        #New text file with the back translation  
        fh = open(text_file_name_new, "w+") 
        fh_rus = open(text_file_name_new_rus, "w+") 

        fh.write(source_out[0]+"\n"+final_english)
        fh_rus.write(source_out[0]+"\n"+final_rus)



    

if __name__ == '__main__': 


          
    print('Enter the text folder path') 
  
    #folder_path = ".wav/"

    folder_path="/home/gsir059/Documents/Aud_Text/text"
    
    

    if not os.path.exists(folder_path):
        exit("not a valid path")
    

  	
    back_translate(folder_path)