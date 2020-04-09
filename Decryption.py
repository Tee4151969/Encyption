import sys
import string
import os
import csv
from cryptography.fernet import Fernet
import random
def randomValue(Text):
    TextResult=''
    Textall=string.ascii_letters
    Textlower=string.ascii_lowercase
    Textupper=string.ascii_uppercase
    Textnumber ="0123456789"

    for elem in Text:
        if elem.isupper():
            TextResult += (random.choice(Textupper.replace(elem,"")))
        elif elem.islower():
            TextResult += (random.choice(Textlower.replace(elem,"")))
        elif elem.isnumeric():
            TextResult += (random.choice(Textnumber.replace(elem,"")))
        else:
            TextResult += elem
    return TextResult




filename = sys.argv[1]
#"D:/Python/Project/PDPA/0beac124-681b-4b70-94dd-bd5d0839f492.config"
key = sys.argv[2]
#"DP5O-6Cvu5N94PzReWnQPe0CQp235NTa9JqKvLoHoOg="

f = open(filename, "r")
spValue = ""
spColumn = ""
keyvalue = ""
columnvalue = ""
pathvalue = ""
pathencodevalue=""
pathfilename = ""
pathupload = ""
isCrack =False
while True:
    line = f.readline()
    if (line.strip()):  # row not blank
        if (line.find("Key") > -1):
            spValue = line.split(" #=# ")
            keyvalue = spValue[1]
        elif (line.find("Column") > -1):
            spValue = line.split(" #=# ")
            columnvalue = spValue[1]
        elif (line.find("Path") > -1):
            spValue = line.split(" #=# ")
            pathvalue = spValue[1]
        elif (line.find("Result") > -1):
            spValue = line.split(" #=# ")
            pathencodevalue = spValue[1]
    if not line:
        break
f.close()

spColumn = columnvalue.replace("\n", "").split(",")
pathfilename = pathencodevalue.replace("\\", "/").replace("\n", "")
pathupload = pathvalue.replace("\\", "/").replace("\n", "")

filenamesw = os.path.basename(pathfilename)
pathnamesw = (os.path.abspath(os.path.join(pathupload, os.pardir)))

filenamecsv = pathnamesw + "/" + filenamesw

keybyte = keyvalue.encode()
cipher_suite = Fernet(keybyte)
if (key.replace("\n", "") == keyvalue.replace("\n", "")):
    isCrack=True
else:
    isCrack=False

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
                    cipher_text = cipher_suite.decrypt(str(row[col]).encode())
                    plain_text = cipher_text.decode("utf-8")
                    if (isCrack):
                        read_to_write.append(plain_text)
                    else:
                        read_to_write.append(randomValue(plain_text))
                else:
                    read_to_write.append(row[col])
            writer.writerow(read_to_write)
        if not line:
            break
    fr.close()
fw.close()
 
print(filenamesw)
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