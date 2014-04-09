import MySQLdb
db = MySQLdb.connect(host="localhost",user="gojones26", passwd="",db="financial_data")
cur = db.cursor()
cur.execute("DELETE FROM bids")
cur.execute("DELETE FROM asks")
db.commit()

