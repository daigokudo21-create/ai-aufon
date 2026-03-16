def calc_profit(buy, sell, repair):
    fee = sell * 0.10
    shipping = 300
    profit = sell - buy - repair - fee - shipping
    return int(profit)
