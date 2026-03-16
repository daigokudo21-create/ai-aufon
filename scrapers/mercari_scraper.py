import re
import requests
from bs4 import BeautifulSoup
from cache_store import get_cached_price, set_cached_price

def get_mercari_price(keyword):
    cached = get_cached_price(keyword)
    if cached is not None:
        return cached

    url = f"https://jp.mercari.com/search?keyword={keyword}&status=sold_out"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        return 0

    prices = []

    for text in soup.stripped_strings:
        if "¥" in text or "￥" in text:
            m = re.search(r"[¥￥]\s*([\d,]+)", text)
            if m:
                try:
                    prices.append(int(m.group(1).replace(",", "")))
                except:
                    pass

    prices = [p for p in prices if 1000 <= p <= 300000]
    prices = sorted(set(prices))

    if not prices:
        return 0

    sample = prices[:20]
    mid = len(sample) // 2

    if len(sample) % 2 == 1:
        price = sample[mid]
    else:
        price = int((sample[mid - 1] + sample[mid]) / 2)

    set_cached_price(keyword, price)
    return price
