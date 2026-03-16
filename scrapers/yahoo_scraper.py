import requests
from bs4 import BeautifulSoup

EXCLUDE_WORDS = [
    "新品",
    "未使用",
    "新品未使用",
]

def get_yahoo_items(keyword):
    url = f"https://auctions.yahoo.co.jp/search/search?p={keyword}&fixed_price=1"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        return []

    items = []

    for item in soup.select("li.Product")[:50]:
        try:
            title = item.select_one("h3").text.strip()
            price_text = item.select_one(".Product__priceValue").text
            price = int(price_text.replace("円", "").replace(",", ""))
            link = item.select_one("a")["href"]
        except:
            continue

        if any(word in title for word in EXCLUDE_WORDS):
            continue

        items.append({
            "title": title,
            "price": price,
            "url": link
        })

    return items[:30]
