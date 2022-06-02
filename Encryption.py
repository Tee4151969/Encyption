import sys
import string
import csv
from np import numpy
from pd import pandas
from cryptography.fernet import Fernet

filename =sys.argv[1] #"c6c44c0c-fd9f-42d2-a773-9668328958fd.config"
filenamecsv = filename.replace(".config",".csv")

f = open(filename, "r")
read_to_write=[]
spValue=""
spColumn=""
keyvalue=""
columnvalue=""
pathvalue= ""
pathfilename=""
while True:
    line = f.readline()
    if (line.strip()): #row not blank
        if (line.find("Key")>-1):
            spValue=line.split(" #=# ")
            keyvalue=spValue[1]
        elif (line.find("Column")>-1):
            spValue=line.split(" #=# ")
            columnvalue = spValue[1]
        elif (line.find("Path")>-1):
            spValue = line.split(" #=# ")
            pathvalue = spValue[1]
    if not line:
        break

f.close()

spColumn = columnvalue.replace("\n","").split(",")
pathfilename=pathvalue.replace("\\", "/").replace("\n","")
keybyte = keyvalue.encode()
cipher_suite = Fernet(keybyte)

fw= open(filenamecsv, 'w', newline='')
with fw:
    writer = csv.writer(fw)
    frhead = open(pathfilename, "r")
    readerhead = csv.DictReader(frhead, delimiter=',')
    headers = next(readerhead, None)
    writer.writerow(headers)
    frhead.close()

    fr = open(pathfilename, "r")
    while True:
        reader = csv.DictReader(fr, delimiter=',')
        for row in reader:
            read_to_write = []
            for col in row:
                find = False
                for text in spColumn:
                    if col == text:
                        find = True
                        break
                if (find):
                    cipher_text = cipher_suite.encrypt(row[col].encode("utf-8"))
                    read_to_write.append(cipher_text.decode("utf-8"))
                else:
                    read_to_write.append(row[col])
            writer.writerow(read_to_write)
        if not line:
            break
    fr.close()
fw.close()
with open(filename, "a") as myfile:
    myfile.write("Result #=# " + filenamecsv)
myfile.close()

print(filename)
"""

 read_to_write=""
            for col in row:
                for column in spColumn:
                    cipher_text = cipher_suite.encrypt(str(row[column]).encode())
                    if (read_to_write !=""):
                        read_to_write += ","
                    read_to_write += str(row[column])
                    if (read_to_write !=""):
                        read_to_write += ","
                    read_to_write += str(cipher_text)
            writer.writerow(({read_to_write}))
            
line = fr.readline()
if (line.strip()):  # row not blank
    cipher_text = cipher_suite.encrypt(line.encode())
     cipher_text = cipher_suite.encrypt(str(row[int(column)]).encode())
            print(row[int(column)] + "," + str(cipher_text)+","+ str(cipher_suite.decrypt(cipher_text)))
    print(cipher_text)

for column in row:
    cipher_text = cipher_suite.encrypt(str(column).encode())
    print(cipher_text)"""