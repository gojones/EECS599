import sqlite3
conn = sqlite3.connect('option_pricing_data.db')
c = conn.cursor()
for row in c.execute('SELECT * FROM order_book'):
    print row

