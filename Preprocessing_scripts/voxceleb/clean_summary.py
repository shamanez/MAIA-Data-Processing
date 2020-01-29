import csv
with open('summary_out.csv') as inp, open('summary_85plus.csv','w') as out:
    writer = csv.writer(out)
    for row in csv.reader(inp):
       if float(row[2]) >= 0.85:
            writer.writerow(row)
