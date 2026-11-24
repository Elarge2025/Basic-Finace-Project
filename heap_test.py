import heapq

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
# s5 = Order(5, True, 10, 97)
s6 = Order(6, True, 10, 101) 
s7 = Order(7, True, 10, 99)
# s8 = Order(8, False, 10, 96)

sell_heap = []
buy_heap = []

heapq.heappush(sell_heap, (s1.stock_price, s1.number, s1))
heapq.heappush(sell_heap, (s2.stock_price, s2.number, s2))
heapq.heappush(sell_heap, (s3.stock_price, s3.number, s3))
heapq.heappush(buy_heap, (-s4.stock_price, s4.number, s4))
heapq.heappush(buy_heap, (-s6.stock_price, s6.number, s6))
heapq.heappush(buy_heap, (-s7.stock_price, s7.number, s7))

while sell_heap:
    best = heapq.heappop(sell_heap)[2]
    print(f"매도 {best.number}번 주문: {best.stock_price}원")

while buy_heap:
    best = heapq.heappop(buy_heap)[2]
    print(f"매수 {best.number}번 주문: {best.stock_price}원")
    