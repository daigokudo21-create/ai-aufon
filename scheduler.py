from apscheduler.schedulers.background import BackgroundScheduler
from scrapers.yahoo_scraper import get_yahoo_items
from scrapers.mercari_scraper import get_mercari_price
from analysis.profit_calc import calc_profit
from analysis.title_classifier import detect_model, detect_damage
from parts_db import PARTS_DB
from result_store import save_results

MODELS = ["iphone11", "iphone12", "iphone13", "iphone14"]

def build_results():
    results = []

    for search_model in MODELS:
        sell_price = get_mercari_price(search_model)

        if sell_price <= 0:
            continue

        items = get_yahoo_items(search_model)

        for item in items:
            model = detect_model(item["title"]) or search_model
            damage = detect_damage(item["title"])

            repair = PARTS_DB.get(model, {}).get(damage, 0)
            profit = calc_profit(item["price"], sell_price, repair)

            results.append({
                "title": item["title"],
                "model": model,
                "damage": damage,
                "buy": item["price"],
                "repair": repair,
                "sell": sell_price,
                "profit": profit,
                "url": item["url"],
            })

    results = sorted(results, key=lambda x: x["profit"], reverse=True)
    save_results(results)
    print(f"[Cache] saved {len(results)} results")

def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(build_results, "interval", minutes=5)
    scheduler.start()

    # 起動直後に1回作る
    try:
        build_results()
    except Exception as e:
        print("initial build error:", e)
