
import requests
from bs4 import BeautifulSoup

def get_mercari_price(keyword):

    url=f"https://jp.mercari.com/search?keyword={keyword}&status=sold_out"

    headers={"User-Agent":"Mozilla/5.0"}

    r=requests.get(url,headers=headers)

    soup=BeautifulSoup(r.text,"html.parser")

    prices=[]

    for p in soup.select("span[data-testid='price']")[:20]:

        try:
            price=int(p.text.replace("¥","").replace(",",""))
            prices.append(price)
        except:
            pass

    if len(prices)==0:
        return 0

    return int(sum(prices)/len(prices))
