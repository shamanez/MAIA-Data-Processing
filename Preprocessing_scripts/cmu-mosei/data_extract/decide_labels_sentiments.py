import os
import csv
import wave
import sys
import numpy as np
import pandas as pd
import glob
import array
import glob


branch='label_file_unknown.csv'
score_csv='./sentiment_final_labels/' + branch
destination='./sentiment_final_labels/decided/'


final_header_label = ['FileName','seven_class','binary']

label_file=open(destination+branch, 'wt', newline ='')
writer_final = csv.writer(label_file, delimiter=',')
writer_final.writerow(i for i in final_header_label)





def get_indexes_max_value(my_list):
    max_value = max(my_list)
    if my_list.count(max_value) > 1:
        return [i for i, x in enumerate(my_list) if x == max(my_list)]
    else:
        return [my_list.index(max(my_list))]






zx=0
with open(score_csv) as f:
    cf = csv.reader(f)
    for row in cf:
      
        if row[0]=='FileName':
            
            continue
           
        
        else:

            zx=zx+1

            example_id=row[0]
            sentiment_score=float(row[1])
  

            if sentiment_score < -2:
                    res = -3
            elif -2 <= sentiment_score and sentiment_score < -1:
                    res = -2
            elif -1 <= sentiment_score and sentiment_score < 0:
                    res = -1
            elif 0 <= sentiment_score and sentiment_score <= 0:
                    res = 0
            elif 0 < sentiment_score and sentiment_score <= 1:
                    res = 1
            elif 1 < sentiment_score and sentiment_score <= 2:
                    res = 2
            elif sentiment_score > 2:
                    res = 3



            seven_class=res


            if sentiment_score<0:
                binary_score=0

            elif sentiment_score>0:
                binary_score=1
            
            elif sentiment_score==0:
                binary_score='non'



         
            combined_row_final=[example_id]+[seven_class]+[binary_score]
            writer_final.writerow(combined_row_final)
               

print(zx+1)    