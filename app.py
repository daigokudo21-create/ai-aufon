from flask import Flask, render_template
from scrapers.yahoo_scraper import get_yahoo_items
from scrapers.mercari_scraper import get_mercari_price
from scrapers.arps_scraper import get_arps_price
from analysis.profit_calc import calc_profit
from analysis.rotation_rate import get_rotation

app = Flask(__name__)

FALLBACK_PARTS = {
    "screen": 3000,
    "battery": 1500,
    "camera": 2500,
    "camera_glass": 800,
    "unknown": 0,
}

def detect_damage_from_title(title: str) -> str:
    t = title.lower()
    if "画面" in t or "液晶" in t or "割れ" in t:
        return "screen"
    if "バッテリー" in t:
        return "battery"
    if "カメラガラス" in t or "カメラ ガラス" in t:
        return "camera_glass"
    if "カメラ" in t:
        return "camera"
    return "unknown"

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/")
def index():
    model = "iphone11"

    try:
        sell_price = get_mercari_price(model)
    except:
        sell_price = 0

    try:
        rotation = get_rotation(model)
    except:
        rotation = 0

    try:
        items = get_yahoo_items(model)
    except:
        items = []

    results = []

    for item in items[:10]:
        damage = detect_damage_from_title(item["title"])

        try:
            repair = get_arps_price(model, damage)
            if not repair:
                repair = FALLBACK_PARTS.get(damage, 0)
        except:
            repair = FALLBACK_PARTS.get(damage, 0)

        profit = calc_profit(item["price"], sell_price, repair)

        results.append({
            "title": item["title"],
            "buy": item["price"],
            "repair": repair,
            "sell": sell_price,
            "profit": profit,
            "rotation": rotation
        })

    results = sorted(results, key=lambda x: x["profit"], reverse=True)

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
