import base64
import string
import datetime
import random
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from flask import Flask, json
import time
from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, json, Response, jsonify
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app)

def randomValue(Text):
    TextResult = ''
    Textall = string.ascii_letters
    Textlower = string.ascii_lowercase
    Textupper = string.ascii_uppercase
    Textnumber = "0123456789"
    TextThai = "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮ"
    for elem in Text:
        if elem.isupper():
            TextResult += (random.choice(Textupper.replace(elem, "")))
        elif elem.islower():
            TextResult += (random.choice(Textlower.replace(elem, "")))
        elif elem.isnumeric():
            TextResult += (random.choice(Textnumber.replace(elem, "")))
        elif pythai.isthai(str(elem)):
            TextResult += (random.choice(TextThai.replace(elem, "")))
        else:
            TextResult += elem
    return TextResult


@app.route('/key/<param>', methods=['GET'])
def generate_key(param: None):
    """Example endpoint returning a response message
       This is using docstrings for specifications.
       ---
       parameters:
         - name: param
           in: path
           type: string
           required: true
       definitions:
         param:
           type: string
       responses:
         200:
           description: A response message
       """
    start_time = (time.strftime("%b %d %Y %H:%M:%S"))
    password_provided = param  # This is input in the form of a string
    password = password_provided.encode()  # Convert to type bytes
    strdate = str(datetime.datetime.now())
    string = strdate.replace("-", "").replace(":", "").replace(".", "").replace(" ", "")
    position = random.randint(1, len(string))
    character = '*'
    salt = string[:position] + character + string[position + 1:]
    # salt = b'salt_' CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt.encode(),
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once
    end_time = (time.strftime("%b %d %Y %H:%M:%S"))
    print(key.decode("utf-8"))
    new_row = {'keyDecode': param, 'keyEncode': key.decode("utf-8"), 'start': start_time, 'end': end_time}
    return json.dumps(new_row)


@app.route('/Encryption/<key>/<param>', methods=['GET'])
def encryption(key: None, param: None):
    """Example endpoint returning a response message
           This is using docstrings for specifications.
           ---
           parameters:
             - name: key
               in: path
               type: string
               required: true
             - name: param
               in: path
               type: string
               required: true
           definitions:
             key:
               type: string
             param:
               type: string
           responses:
             200:
               description: A response message
           """
    print(key)
    print(param)
    keybyte = key.encode()
    cipher_suite = Fernet(keybyte)
    cipher_text = cipher_suite.encrypt(param.encode("utf-8"))
    print(cipher_text)

    value_cipher = "dd"
    new_row = {'key': key, 'value': param, 'value_cipher': value_cipher, 'cipher': cipher_text.decode("utf-8")}
    print(new_row)
    return json.dumps(new_row)


@app.route('/decryption/<key>/<param>', methods=['GET'])
def decryption(key: None, param: None):
    """Example endpoint returning a response message
           This is using docstrings for specifications.
           ---
           parameters:
             - name: key
               in: path
               type: string
               required: true
             - name: param
               in: path
               type: string
               required: true
           definitions:
             key:
               type: string
             param:
               type: string
           responses:
             200:
               description: A response message
           """
    cipher_suite = None
    try:
        f = Fernet(key)
    except InvalidToken:
        f = None
    print(f)
    if not f is None:
        try:
            decrypted_bytes = f.decrypt(param.encode("utf-8"))
        except InvalidToken:
            decrypted_bytes = None  # TODO(kmullins): Shall we log this case? Is it expected?
        if not decrypted_bytes is None:
            decrypted_string = decrypted_bytes.decode()  # bytes -> str
        else:
            decrypted_string = "encryption is not support"
    else:
        key = "key is not support"

    new_row = {'key': key, 'value': param, 'value_cipher': decrypted_string}
    print(new_row);
    return json.dumps(new_row)


app.run(debug=True, host='0.0.0.0', port=80)  #
