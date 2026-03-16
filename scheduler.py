
from apscheduler.schedulers.background import BackgroundScheduler
from scrapers.yahoo_scraper import get_yahoo_items

def scan_market():
    print("scan")
    items=get_yahoo_items("iphone11")
    print(len(items))

def start_scheduler():
    scheduler=BackgroundScheduler()
    scheduler.add_job(scan_market,"interval",minutes=5)
    scheduler.start()
