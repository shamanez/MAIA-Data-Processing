import os
import csv

source_list = './aud2text_shuffled.csv'
dest_list = './face_r_shuffled.csv'
result = list()
count = 0

with open(source_list) as shuffled:
    readCSV = csv.reader(shuffled, delimiter=',')
    for aud in readCSV:
        count += 1
        print(count)    
        new = aud[0].split('/')[-3:]
        new[-1] = new[-1][:-4] + '.mp4'
        new = '/'.join(new)
        new = os.path.join('./video/dev/mp4/',new)
        result.append(new) 

with open(dest_list, 'a') as fd:
    writer = csv.writer(fd)
    for aud in result:
        count -= 1
        print(count)
        writer.writerow([aud])