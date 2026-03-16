from flask import Flask, render_template, request
from scheduler import start_scheduler
from scrapers.yahoo_scraper import get_yahoo_items
from scrapers.mercari_scraper import get_mercari_price
from analysis.profit_calc import calc_profit
from analysis.title_classifier import detect_model, detect_damage
from parts_db import PARTS_DB

app = Flask(__name__)

start_scheduler()

MODELS = ["iphone11", "iphone12", "iphone13", "iphone14"]

@app.route("/")
def index():
    selected_model = request.args.get("model", "")
    selected_damage = request.args.get("damage", "")
    profit_filter = request.args.get("profit", "")

    results = []

    targets = MODELS if not selected_model else [selected_model]

    for search_model in targets:
        sell_price = get_mercari_price(search_model)

        # 売値が0ならその機種は飛ばす
        if sell_price <= 0:
            continue

        items = get_yahoo_items(search_model)

        for item in items:
            model = detect_model(item["title"]) or search_model
            damage = detect_damage(item["title"])

            repair = PARTS_DB.get(model, {}).get(damage, 0)
            profit = calc_profit(item["price"], sell_price, repair)

            row = {
                "title": item["title"],
                "model": model,
                "damage": damage,
                "buy": item["price"],
                "repair": repair,
                "sell": sell_price,
                "profit": profit,
                "url": item["url"],
            }

            results.append(row)

    if selected_damage:
        results = [r for r in results if r["damage"] == selected_damage]

    if profit_filter == "plus":
        results = [r for r in results if r["profit"] > 0]
    elif profit_filter == "5000":
        results = [r for r in results if r["profit"] >= 5000]
    elif profit_filter == "10000":
        results = [r for r in results if r["profit"] >= 10000]

    results = sorted(results, key=lambda x: x["profit"], reverse=True)

    return render_template(
        "index.html",
        results=results,
        selected_model=selected_model,
        selected_damage=selected_damage,
        profit_filter=profit_filter
    )

@app.route("/healthz")
def healthz():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
