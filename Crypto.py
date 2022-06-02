
import cx_Oracle
connection = cx_Oracle.connect("dvauxappo", "dn529wng", "tedwdev")
cursor = connection.cursor()
cursor.execute("""select to_char(sysdate, 'dd-mon-yyyy') from dual""")
for cdate in cursor:
    print("Today the date is ", cdate)

from cryptography.fernet import Fernet
key = b'DP5O-6Cvu5N94PzReWnQPe0CQp235NTa9JqKvLoHoOg='

cipher_suite = Fernet(key)
cipher_text = cipher_suite.encrypt("ทดสdddsafอบ".encode("utf-8"))

cipher_abc ='gAAAAABegL5Um6a4lhHyzCS4XGx1zS8nrfK5onQ6XTGAF1fzFdkF5GnrflRS3GHz8MVwefrAqME9_7N1FdakI4kC9YB0f-Dp4A=='.encode()
xx = Fernet(key)
plain_text  = xx.decrypt(cipher_abc)
plain_textX = xx.decrypt(cipher_text)
print(plain_textX.decode("utf-8"))
print(plain_text.decode("utf-8"))
print(cipher_text.decode("utf-8"))

