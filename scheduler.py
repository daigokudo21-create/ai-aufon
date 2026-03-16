from apscheduler.schedulers.background import BackgroundScheduler
from scrapers.yahoo_scraper import get_yahoo_items
from scrapers.mercari_scraper import get_mercari_price

MODELS = ["iphone11", "iphone12", "iphone13", "iphone14"]

def scan_yahoo():
    for model in MODELS:
        items = get_yahoo_items(model)
        print(f"[Yahoo] {model}: {len(items)} items")

def refresh_mercari():
    for model in MODELS:
        price = get_mercari_price(model)
        print(f"[Mercari] {model}: {price}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(scan_yahoo, "interval", minutes=5)
    scheduler.add_job(refresh_mercari, "interval", hours=1)
    scheduler.start()
