
import requests
from bs4 import BeautifulSoup

def get_rotation(keyword):

    url=f"https://jp.mercari.com/search?keyword={keyword}&status=sold_out"

    headers={"User-Agent":"Mozilla/5.0"}

    r=requests.get(url,headers=headers)

    soup=BeautifulSoup(r.text,"html.parser")

    sold=len(soup.select("span[data-testid='price']"))

    url2=f"https://jp.mercari.com/search?keyword={keyword}"

    r2=requests.get(url2,headers=headers)

    soup2=BeautifulSoup(r2.text,"html.parser")

    listing=len(soup2.select("span[data-testid='price']"))

    if listing==0:
        return 0

    return round((sold/listing)*100,1)
