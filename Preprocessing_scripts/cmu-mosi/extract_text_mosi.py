
import csv
import os

from mosi_fold import *

TEXT_PATH='./Transcript/Segmented'

base_dir='./Transcript/ready/'


for filename in os.listdir(TEXT_PATH):

  
    with open(TEXT_PATH + '/' + filename, 'r') as combined:

     
        for line in combined:

 
    
            if '_DELIM_' in line:
                print(line.split('_'))


                
                single_filename = filename.split('.')[0]+"_"+line.split('_')[0]
         
                
                
                
                if filename.split('.')[0] in standard_train_fold:
                    fold_dir='train/'
                
                elif filename.split('.')[0] in standard_test_fold:
                    fold_dir='test/'
                
                elif filename.split('.')[0] in standard_valid_fold:
                    fold_dir='valid/'
                
                else:
                    fold_dir='un/'

                
                text=line.split('_')[-1]

                

                if text[0]==" ":
                	lower_text=text[1]+text[2:].lower()


                else:

                	lower_text=text[0]+text[1:].lower()



            
                with open(base_dir+fold_dir + single_filename + ".txt", 'w') as out:
                    #print(line.split('_')[-1])
                    out.write(lower_text)

                
            else:
                print(line)
                exit("---------")