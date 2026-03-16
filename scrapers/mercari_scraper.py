import re
import requests
from bs4 import BeautifulSoup
from cache_store import get_cached_price, set_cached_price

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7",
}

FALLBACK_PRICES = {
    "iphone11": 23000,
    "iphone12": 32000,
    "iphone13": 43000,
    "iphone14": 56000,
}

def _extract_prices_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    prices = []

    # まず通常の価格表示を拾う
    for text in soup.stripped_strings:
        m = re.search(r"[¥￥]\s*([\d,]+)", text)
        if m:
            try:
                price = int(m.group(1).replace(",", ""))
                if 1000 <= price <= 300000:
                    prices.append(price)
            except:
                pass

    # 重複除去
    prices = sorted(set(prices))
    return prices

def get_mercari_price(keyword):
    cached = get_cached_price(keyword)
    if cached is not None and cached > 0:
        return cached

    url = f"https://jp.mercari.com/search?keyword={keyword}&status=sold_out"

    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        prices = _extract_prices_from_html(r.text)
    except:
        prices = []

    # 取れなかったら通常検索も試す
    if not prices:
        try:
            url2 = f"https://jp.mercari.com/search?keyword={keyword}"
            r2 = requests.get(url2, headers=HEADERS, timeout=20)
            prices = _extract_prices_from_html(r2.text)
        except:
            prices = []

    if prices:
        sample = prices[:20]
        mid = len(sample) // 2

        if len(sample) % 2 == 1:
            price = sample[mid]
        else:
            price = int((sample[mid - 1] + sample[mid]) / 2)

        set_cached_price(keyword, price)
        return price

    # 最後は固定相場に逃がす
    fallback = FALLBACK_PRICES.get(keyword, 0)
    if fallback > 0:
        set_cached_price(keyword, fallback)
    return fallback
