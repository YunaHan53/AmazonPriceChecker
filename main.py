import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests

load_dotenv()

AmazonURL = os.getenv("AmazonURL")
response = requests.get(AmazonURL)
amazon_page = response.text

soup = BeautifulSoup(amazon_page, 'html.parser')

product_title = soup.find("div", id="title_feature_div")
product_price = soup.find("span", class_="aok-offscreen")
price_num = product_price.text.split("$")[1]
print(price_num)