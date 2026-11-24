import sqlite3
conn = sqlite3.connect("trades.db")
conn.execute("CREATE TABLE IF NOT EXISTS trades (trade_id INTEGER PRIMARY KEY, buy_order INTEGER, sell_order INTEGER, price INTEGER, quantity INTEGER)")
conn.commit()


class Order:
    def __init__(self, number, is_buy, order_quantity, stock_price):
        self.number = number
        self.is_buy = is_buy
        self.order_quantity = order_quantity
        self.stock_price = stock_price

s1 = Order(1, False, 10, 100)
s2 = Order(2, False, 10, 98)
s3 = Order(3, False, 10, 98)
s4 = Order(4, True, 10, 99)
s5 = Order(5, True, 10, 97)
s6 = Order(6, True, 10, 101) 
s7 = Order(7, True, 10, 90)
s8 = Order(8, False, 10, 96)

buy_orders = []
sell_orders = []


def find_best_sell(sell_orders):
    if len(sell_orders) == 0:
        return None
    
    best = sell_orders[0]
    for order in sell_orders:
        if order.stock_price < best.stock_price:
            best = order
    return best

def find_best_buy(buy_orders):
    if len(buy_orders) == 0:
        return None
    best = buy_orders[0]
    for order in buy_orders:
        if order.stock_price > best.stock_price:
            best = order
    return best


def submit(order):
    if order.is_buy:
        while order.order_quantity > 0:                     # 내 주문이 남아 있는 동안
            best = find_best_sell(sell_orders)
            if best is None or order.stock_price < best.stock_price:    # 멈추는 조건 (상대 없음 or 가격 안 맞음)
                break
            a = min(order.order_quantity, best.order_quantity) # 체결 수량 구하기 (min 사용)
            print(f"{order.number}번 매수 주문 체결 완료: {best.number}번, {best.stock_price}원, {a}주") # 체결 출력
            conn.execute("INSERT INTO trades (buy_order, sell_order, price, quantity) VALUES (?, ?, ?, ?)", (order.number, best.number, best.stock_price, a))
            best.order_quantity -= a # 양쪽 수량 빼기
            order.order_quantity -= a
            if best.order_quantity <= 0: # best 수량이 0이면 sell_orders에서 빼기
                sell_orders.remove(best)

        if order.order_quantity > 0: # 반복이 끝난 뒤: 남은 수량이 있으면 buy_orders에 넣기
            buy_orders.append(order)
    else:
        while order.order_quantity > 0:
            best = find_best_buy(buy_orders)
            if best is None or order.stock_price > best.stock_price:
                break
            a = min(order.order_quantity, best.order_quantity)
            print(f"{order.number}번 매도 주문 체결 완료: {best.number}번, {best.stock_price}원, {a}주") # 체결 출력
            conn.execute("INSERT INTO trades (buy_order, sell_order, price, quantity) VALUES (?, ?, ?, ?)", (best.number, order.number, best.stock_price, a))

            best.order_quantity -= a
            order.order_quantity -= a
            if best.order_quantity <= 0:
                buy_orders.remove(best)
        if order.order_quantity > 0 :
            sell_orders.append(order)


x = Order(1, True, 3, 99)
y = Order(2, True, 5, 99)
z = Order(3, True, 10, 97)
new = Order(4, False, 10, 98)
submit(x)
submit(y)
submit(z)
submit(new)
print("남은 매수:", [(o.number, o.stock_price, o.order_quantity) for o in buy_orders])
print("남은 매도:", [(o.number, o.stock_price, o.order_quantity) for o in sell_orders])
conn.commit()
rows = conn.execute("SELECT * FROM trades").fetchall()
print(rows)
conn.close()