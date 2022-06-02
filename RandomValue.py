import random
import string
import sys
import numbers
def RandomText(Text):
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