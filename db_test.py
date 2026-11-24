import sqlite3

conn = sqlite3.connect("trades.db")
conn.execute("CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, buy_order INTEGER, sell_order INTEGER, price INTEGER, quantity INTEGER)")
conn.commit()
b= 5
s= 3
p = 97
q = 2
# conn.execute("INSERT INTO trades (buy_order, sell_order, price, quantity) VALUES (?, ?, ?, ?)", (b, s, p, q))
conn.commit()
rows = conn.execute("SELECT sell_order, SUM(quantity) FROM trades GROUP BY sell_order;").fetchall()
print(rows)
rows = conn.execute("SELECT * FROM trades").fetchall()
print(rows)
conn.close()