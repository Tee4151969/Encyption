import base64
import os
import sys
import datetime
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

password_provided = sys.argv[1] # This is input in the form of a string
password = password_provided.encode() # Convert to type bytes

strdate = str(datetime.datetime.now())
string = strdate.replace("-","").replace(":","").replace(".","").replace(" ","")
position  = random.randint(1,len(string))
character = '*'

salt = string[:position] + character + string[position+1:]
#salt = b'salt_' CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt.encode(),
    iterations=100000,
    backend=default_backend()
)
key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
#key.decode(encoding="utf-8")
#key.decode(encoding)

print(key.decode("utf-8"))
