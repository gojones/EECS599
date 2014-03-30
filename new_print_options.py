import MySQLdb
db = MySQLdb.connect(host="localhost", user="gojones26", passwd="",
                     db="financial_data")
cur = db.cursor()
cur.execute("SELECT * FROM options")
print cur.fetchall()

