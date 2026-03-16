import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

EXCLUDE_WORDS = [
    "新品",
    "未使用",
    "新品未使用",
]

def get_yahoo_items(keyword):
    url = f"https://auctions.yahoo.co.jp/search/search?p={quote(keyword)}&fixed_price=1"

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[yahoo] request error keyword={keyword}: {e}")
        return []

    items = []

    for item in soup.select("li.Product")[:30]:
        try:
            title_el = item.select_one("h3")
            price_el = item.select_one(".Product__priceValue")
            link_el = item.select_one("a")

            if not title_el or not price_el or not link_el:
                continue

            title = title_el.get_text(strip=True)
            price_text = price_el.get_text(strip=True)
            price = int(price_text.replace("円", "").replace(",", "").replace(" ", ""))
            link = link_el.get("href", "").strip()

            if not title or not link:
                continue
        except Exception:
            continue

        if any(word in title for word in EXCLUDE_WORDS):
            continue

        items.append({
            "title": title,
            "price": price,
            "url": link
        })

    print(f"[yahoo] keyword={keyword} items={len(items)}")
    return items
