import Environment
import RandomValue
import cx_Oracle
from cryptography.fernet import Fernet
key = b'DP5O-6Cvu5N94PzReWnQPe0CQp235NTa9JqKvLoHoOg='
cipher_suite = Fernet(key)

connection = cx_Oracle.connect("tedwcisappo", "Etl!428Ks", "tedwdev")
cursor = connection.cursor()
cursor.execute("""select * from ztee_pdpa_true_product_token""")
for row in cursor:
    cipher_text = cipher_suite.decrypt(str(row[1]).encode())
    plain_text = cipher_text.decode("utf-8")
    print('Original Text=' + plain_text)
    print('Encryption Text =' +RandomValue.RandomText(plain_text))

cursor.close()
