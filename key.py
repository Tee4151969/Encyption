import base64
import sys
import datetime
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import Flask, request, render_template, session, redirect, json
import time
from pandas.io.json import json_normalize
import pandas as pd
import uuid
import hashlib
from googletrans import Translator
import pythainlp.util as pyUtil

def generate_key(param : None):
    start_time = (time.strftime("%b %d %Y %H:%M:%S"))
    password_provided = param # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    strdate = str(datetime.datetime.now())
    string = strdate.replace("-","").replace(":","").replace(".","").replace(" ","")
    position = random.randint(1,len(string))
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
    end_time = (time.strftime("%b %d %Y %H:%M:%S"))
    print(key.decode("utf-8"))
    new_row = {'keyDecode': param, 'keyEncode': key.decode("utf-8"), 'start': start_time, 'end': end_time}
    return json.dumps(new_row)

#app.run(debug=True, host='0.0.0.0', port=80)
