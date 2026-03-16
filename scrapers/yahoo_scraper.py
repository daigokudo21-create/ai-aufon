
import requests
from bs4 import BeautifulSoup

def get_yahoo_items(keyword):

    url=f"https://auctions.yahoo.co.jp/search/search?p={keyword}&fixed_price=1"

    headers={"User-Agent":"Mozilla/5.0"}

    r=requests.get(url,headers=headers)

    soup=BeautifulSoup(r.text,"html.parser")

    items=[]

    for item in soup.select("li.Product")[:20]:

        try:

            title=item.select_one("h3").text.strip()

            price=item.select_one(".Product__priceValue").text

            price=int(price.replace("円","").replace(",",""))

            image=item.select_one("img")["src"]

            items.append({
                "title":title,
                "price":price,
                "image":image
            })

        except:
            pass

    return items
