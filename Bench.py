import heapq, random, time

class Order:
    def __init__(self, number, is_buy, order_quantity, stock_price):
        self.number = number; self.is_buy = is_buy
        self.order_quantity = order_quantity; self.stock_price = stock_price

# ---------- 리스트 버전 ----------
def run_list(orders):
    buy_orders, sell_orders = [], []
    def find_best_sell(s):
        if len(s) == 0: return None
        best = s[0]
        for o in s:
            if o.stock_price < best.stock_price: best = o
        return best
    def find_best_buy(b):
        if len(b) == 0: return None
        best = b[0]
        for o in b:
            if o.stock_price > best.stock_price: best = o
        return best
    trades = 0
    for order in orders:
        if order.is_buy:
            while order.order_quantity > 0:
                best = find_best_sell(sell_orders)
                if best is None or order.stock_price < best.stock_price: break
                a = min(order.order_quantity, best.order_quantity); trades += 1
                best.order_quantity -= a; order.order_quantity -= a
                if best.order_quantity <= 0: sell_orders.remove(best)
            if order.order_quantity > 0: buy_orders.append(order)
        else:
            while order.order_quantity > 0:
                best = find_best_buy(buy_orders)
                if best is None or order.stock_price > best.stock_price: break
                a = min(order.order_quantity, best.order_quantity); trades += 1
                best.order_quantity -= a; order.order_quantity -= a
                if best.order_quantity <= 0: buy_orders.remove(best)
            if order.order_quantity > 0: sell_orders.append(order)
    return trades

# ---------- 힙 버전 ----------
def run_heap(orders):
    buy_heap, sell_heap = [], []
    trades = 0
    for order in orders:
        if order.is_buy:
            while order.order_quantity > 0:
                best = sell_heap[0][2] if sell_heap else None
                if best is None or order.stock_price < best.stock_price: break
                a = min(order.order_quantity, best.order_quantity); trades += 1
                best.order_quantity -= a; order.order_quantity -= a
                if best.order_quantity <= 0: heapq.heappop(sell_heap)
            if order.order_quantity > 0: heapq.heappush(buy_heap, (-order.stock_price, order.number, order))
        else:
            while order.order_quantity > 0:
                best = buy_heap[0][2] if buy_heap else None
                if best is None or order.stock_price > best.stock_price: break
                a = min(order.order_quantity, best.order_quantity); trades += 1
                best.order_quantity -= a; order.order_quantity -= a
                if best.order_quantity <= 0: heapq.heappop(buy_heap)
            if order.order_quantity > 0: heapq.heappush(sell_heap, (order.stock_price, order.number, order))
    return trades

def make_orders(n, seed=42):
    rnd = random.Random(seed)
    # 매수는 조금 낮게, 매도는 조금 높게 → 대기열이 쌓이면서 일부 체결
    out = []
    for i in range(1, n + 1):
        is_buy = rnd.random() < 0.5
        price = rnd.randint(9000, 10100) if is_buy else rnd.randint(9900, 11000)
        out.append(Order(i, is_buy, rnd.randint(1, 100), price))
    return out

for n in [1_000, 10_000, 30_000]:
    t = time.perf_counter(); tl = run_list(make_orders(n)); list_sec = time.perf_counter() - t
    t = time.perf_counter(); th = run_heap(make_orders(n)); heap_sec = time.perf_counter() - t
    print(f"{n:>6}개 | 리스트 {list_sec:8.3f}초 | 힙 {heap_sec:6.3f}초 | {list_sec/heap_sec:6.0f}배 | 체결 {tl}건 / {th}건")