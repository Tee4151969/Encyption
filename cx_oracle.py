import cx_Oracle
connection = cx_Oracle.connect("dvauxappo", "dn529wng", "tedwdev")
cursor = connection.cursor()
cursor.execute("""select to_char(sysdate, 'dd-mon-yyyy') from dual""")
for cdate in cursor:
    print("Today the date is ", cdate)

from cryptography.fernet import Fernet
key = b'fWn9BDrXryrtcxjXhaO2BR9Oc_bS_zk1k4b6aL_0rbI='
cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt(b"0841119142")
plain_text = cipher_suite.decrypt(cipher_text)


xx = Fernet(key)
plain_textX = xx.decrypt(cipher_text)

print(plain_textX.decode("utf-8"))

print(cipher_text.decode("utf-8"))

print(plain_text.decode("utf-8"))
