
from flask import Flask,render_template
from scrapers.yahoo_scraper import get_yahoo_items
from scrapers.mercari_scraper import get_mercari_price
from scrapers.arps_scraper import get_arps_price
from ai.damage_ai import detect_damage
from analysis.profit_calc import calc_profit
from analysis.rotation_rate import get_rotation
from scheduler import start_scheduler

app = Flask(__name__)

start_scheduler()

@app.route("/")
def index():

    model="iphone11"

    sell_price=get_mercari_price(model)
    rotation=get_rotation(model)

    items=get_yahoo_items(model)

    results=[]

    for item in items:

        damage=detect_damage(item["image"])

        repair=get_arps_price(model,damage)

        profit=calc_profit(item["price"],sell_price,repair)

        results.append({
            "title":item["title"],
            "buy":item["price"],
            "repair":repair,
            "sell":sell_price,
            "profit":profit,
            "rotation":rotation
        })

    results=sorted(results,key=lambda x:x["profit"],reverse=True)

    return render_template("index.html",results=results)

if __name__=="__main__":
    app.run(host="0.0.0.0",port=10000)
