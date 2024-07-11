import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import json

print("~ Initiating Web Scraping...")
data=[]
product_links = []
base_url = "https://www.flipkart.com"
url = "https://www.flipkart.com/mens-footwear/mens-casual-shoes/pr?sid=osp%2Ccil%2Ce1f&p%5B%5D=facets.price_range.from%3DMin&p%5B%5D=facets.price_range.to%3D1500&otracker=categorytree&page=1"
page = 1

r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

''' This script is automated to scraping data form all the pages present by extracting the
    number of pages present.
    Number of pages to scrape data can be set manually'''

total_page =(list(map(str, (soup.find("div", class_ = "_1G0WLw").span.string).split()))[-1])
last_page = int(input("Number of pages to scrape data out of " + total_page + " pages : "))
def get_url():
    global url
    global page
    url = url[:-1] + str(page +1)
    page+=1
    return url

while page <= last_page:
    r = requests.get(get_url())
    soup = BeautifulSoup(r.text, "html.parser")
    product_list = soup.find_all("a", class_ = "WKTcLC")
    for product in product_list:
        link = product.get("href")
        product_links.append(link)
    print("* Page", page-1 , "product extraction Complete...")
print("~ All Product Extraction Complete...")

print("~ Initiating product's feature extraction...")
for link in product_links:
    f = requests.get(base_url+link)
    soup = BeautifulSoup(f.text,"html.parser")

    try:
        price=soup.find("div",class_="Nx9bqj").text.replace('\n',"")
    except:
        price = None

    try:
        about=soup.find("span",class_="VU-ZEz").text.replace('\n',"")
    except:
        about=None

    try:
        rating = soup.find("div",class_ = "XQDdHH _1Quie7").text.replace('\n',"")
    except:
        rating=None

    try:
        brand=soup.find("span",class_="mEh187").text.replace('\n',"")
    except:
        brand=None

    shoe = {"Brand":brand, "Price":price, "Rating":rating, "About":about}
    data.append(shoe)
print("~ Feature extraction compleete...\n~ Initiating data conversion...")
df = pd.DataFrame(data)
df.to_csv('product.csv', header=False, index=False)
file = open('product.json', mode='w', encoding='utf-8')
file.write(json.dumps(data))
print("~ Conversion complete...")
print(df)
print("~ Web Scraping Complete...")
