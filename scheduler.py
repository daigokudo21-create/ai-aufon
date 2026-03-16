from scrapers.yahoo_scraper import get_yahoo_items
from result_store import save_results

MODELS = [
    "iPhone X",
    "iPhone XR",
    "iPhone XS",
    "iPhone XS Max",
    "iPhone 11",
    "iPhone 11 Pro",
    "iPhone 11 Pro Max",
    "iPhone 12",
    "iPhone 12 mini",
    "iPhone 12 Pro",
    "iPhone 12 Pro Max",
]

ISSUES = [
    "画面割れ",
    "液晶不良",
    "バッテリー",
    "ジャンク",
]

REPAIR_COSTS = {
    "画面割れ": 8000,
    "液晶不良": 10000,
    "バッテリー": 5000,
    "ジャンク": 12000,
}

SELL_PRICE_TABLE = {
    "iPhone X": 23000,
    "iPhone XR": 26000,
    "iPhone XS": 28000,
    "iPhone XS Max": 33000,
    "iPhone 11": 35000,
    "iPhone 11 Pro": 43000,
    "iPhone 11 Pro Max": 50000,
    "iPhone 12": 47000,
    "iPhone 12 mini": 39000,
    "iPhone 12 Pro": 56000,
    "iPhone 12 Pro Max": 65000,
}

def estimate_sell_price(model):
    return SELL_PRICE_TABLE.get(model, 0)

def build_rankings():
    results = []

    for model in MODELS:
        for issue in ISSUES:
            keyword = f"{model} {issue}"
            yahoo_items = get_yahoo_items(keyword)

            print(f"[scheduler] keyword={keyword} yahoo_items={len(yahoo_items)}")

            for item in yahoo_items:
                buy_price = item["price"]
                repair_cost = REPAIR_COSTS.get(issue, 0)
                sell_price = estimate_sell_price(model)
                profit = sell_price - buy_price - repair_cost

                # 売値が無いものは除外
                if sell_price <= 0:
                    continue

                # 利益が大きくマイナスのものは除外
                if profit < -5000:
                    continue

                results.append({
                    "model": model,
                    "issue": issue,
                    "title": item["title"],
                    "buy_price": buy_price,
                    "repair_cost": repair_cost,
                    "sell_price": sell_price,
                    "profit": profit,
                    "url": item["url"],
                })

    results.sort(key=lambda x: x["profit"], reverse=True)

    print(f"[scheduler] total results={len(results)}")
    save_results(results)
    return results

if __name__ == "__main__":
    build_rankings()
