import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import smtplib
import datetime, time

load_dotenv()

from_email = os.getenv("FROM_EMAIL")
to_email = os.getenv("TO_EMAIL")
password = os.getenv("PASSWORD")
smtp = os.getenv("SMTP_HOST")
AmazonURL = os.getenv("URL")

TARGET = 100.00

def get_product_details(target_price):
    response = requests.get(AmazonURL)
    amazon_page = response.text

    soup = BeautifulSoup(amazon_page, 'html.parser')

    product_title = soup.find("span", id="productTitle").get_text()
    product_price = soup.find("span", class_="aok-offscreen")

    product_name = product_title.split("\n")[0].strip()
    price_no_dollar = float(product_price.text.split("$")[1])

    if price_no_dollar < target_price:
        return f"{product_name},{price_no_dollar}"
    else:
        return None

def send_email(p_title, p_price):
    with smtplib.SMTP(smtp, port=587) as connection:
        # TLS Transport Layer Security - Securing our connection to our email server
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email,
            msg=f"Subject: Product: {p_title} -> Current Price: ${p_price}\n\n"
                f"{p_title} is now ${p_price}\n\n"
                f"Link: {AmazonURL}")


while True:
    # Checks time and runs program at 9:00 daily
    date_time = datetime.datetime.now()
    time_now = date_time.strftime("%H:%M")
    if time_now == "09:00":
        product_details = get_product_details(TARGET)
        title = product_details.split(",")[0]
        price = product_details.split(",")[1]
        send_email(title, price)

        time.sleep(60)
