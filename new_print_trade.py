import MySQLdb
db = MySQLdb.connect(host="localhost", user="gojones26", passwd="",
                     db="financial_data")
cur = db.cursor()
cur.execute("SELECT * FROM last_trade")
print cur.fetchall()

