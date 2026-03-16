
import requests
from bs4 import BeautifulSoup

def get_arps_price(model,part):

    keyword=f"{model} {part}"

    url=f"https://www.arps.shop/search?q={keyword}"

    headers={"User-Agent":"Mozilla/5.0"}

    try:

        r=requests.get(url,headers=headers)

        soup=BeautifulSoup(r.text,"html.parser")

        prices=[]

        for p in soup.select(".price"):

            try:
                price=int(p.text.replace("¥","").replace(",",""))
                prices.append(price)
            except:
                pass

        if len(prices)==0:
            return 0

        return min(prices)

    except:

        return 0
