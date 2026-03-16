from scrapers.yahoo_scraper import get_yahoo_items
from result_store import save_results

MODELS = [
    "iPhone X",
    "iPhone XR",
    "iPhone XS",
    "iPhone 11",
    "iPhone 11 Pro",
    "iPhone 12",
    "iPhone 12 mini",
    "iPhone SE2",
    "iPhone SE3",
]

ISSUES = [
    "画面割れ",
    "ジャンク",
    "液晶不良",
    "バッテリー",
]

REPAIR_COSTS = {
    "画面割れ": 8000,
    "ジャンク": 10000,
    "液晶不良": 9000,
    "バッテリー": 5000,
}

SELL_PRICE_TABLE = {
    "iPhone X": 23000,
    "iPhone XR": 26000,
    "iPhone XS": 28000,
    "iPhone 11": 35000,
    "iPhone 11 Pro": 43000,
    "iPhone 12": 47000,
    "iPhone 12 mini": 39000,
    "iPhone SE2": 22000,
    "iPhone SE3": 32000,
}

def estimate_sell_price(model):
    return SELL_PRICE_TABLE.get(model, 0)

def build_rankings():
    results = []

    for model in MODELS:
        for issue in ISSUES:
            keyword = f"{model} {issue}"
            yahoo_items = get_yahoo_items(keyword)

            for item in yahoo_items:
                buy_price = item["price"]
                repair_cost = REPAIR_COSTS.get(issue, 0)
                sell_price = estimate_sell_price(model)
                profit = sell_price - buy_price - repair_cost

                if sell_price <= 0:
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
