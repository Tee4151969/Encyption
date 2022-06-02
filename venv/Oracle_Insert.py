
import Environment
import cx_Oracle
from cryptography.fernet import Fernet
key = b'DP5O-6Cvu5N94PzReWnQPe0CQp235NTa9JqKvLoHoOg='
cipher_suite = Fernet(key)


intRow=0
connection = cx_Oracle.connect("tedwcisappo", "Etl!428Ks", "tedwdev")
column=[]

cursor_column = connection.cursor()
cursor_column.execute("""SELECT X.COLNO, X.CNAME, X.COLTYPE, X.WIDTH  FROM COL X WHERE X.TNAME = 'ZTEE_PDPA_TRUE_PRODUCT_HASH' """)

for row in cursor_column:
    column.append(row[1])
cursor_column.close()
print(column)
sQL = "INSERT INTO ZTEE_PDPA_TRUE_PRODUCT_TOKEN X VALUES ({},'{}','{}')"
cursorInsert = connection.cursor()
cursor = connection.cursor()
cursor.execute("""select * from ztee_pdpa_true_product_hash""")
for row in cursor:
    cipher_text = cipher_suite.encrypt(row[0].encode("utf-8"))
    intRow += 1
    cursorInsert.execute(sQL.format(intRow,cipher_text.decode("utf-8"),row[1]))
    connection.commit()

cursor.close()
connection.commit()
