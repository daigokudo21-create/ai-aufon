import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# 新品などを除外
EXCLUDE_WORDS = [
    "新品",
    "未使用",
    "新品未使用",
]

def get_yahoo_items(keyword):

    url = f"https://auctions.yahoo.co.jp/search/search?p={keyword}&fixed_price=1"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
    except:
        return []

    items = []

    # 最大30件
    for item in soup.select("li.Product")[:30]:

        try:
            title = item.select_one("h3").text.strip()

            price_text = item.select_one(".Product__priceValue").text
            price = int(price_text.replace("円", "").replace(",", ""))

            link = item.select_one("a")["href"]

        except:
            continue

        # 新品除外
        if any(word in title for word in EXCLUDE_WORDS):
            continue

        items.append({
            "title": title,
            "price": price,
            "url": link
        })

    return items
