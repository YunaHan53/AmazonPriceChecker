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
HEADERS={
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,es;q=0.6,ko;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 OPR/129.0.0.0",
  }
TARGET = 130.00

def get_product_details(target_price):
    """Gets product name and current price from Amazon URL
    Checks current price to see if it's below the target price"""
    response = requests.get(AmazonURL, headers=HEADERS)
    amazon_page = response.text

    soup = BeautifulSoup(amazon_page, 'html.parser')

    product_title = soup.find("span", id="productTitle").get_text()
    product_price = soup.find("span", class_="aok-offscreen").get_text()
    product_name = product_title.split("\n")[0].strip().split(",")[0]
    price_no_dollar = float(product_price.split("$")[1])

    if price_no_dollar < target_price:
        return f"{product_name}=>{product_price}"
    else:
        return None

def send_email(p_title, p_price):
    """Sends email to alert the user if price drops below target price"""
    subject = "Subject: Amazon Price Alert!"
    body    = f"""
    <html>
    <body>
        <h3>Price Drop Alert!</h3>
        <p><b>{p_title}</b> is now <b>{p_price}</b></p>
        <a href="{AmazonURL}">View on Amazon</a>
    </body>
    </html>
    """

    # ← MIME header tells email client to render HTML
    message = f"{subject}\nMIME-Version: 1.0\nContent-Type: text/html\n\n{body}"

    with smtplib.SMTP(smtp, port=587) as connection:
        # TLS Transport Layer Security - Securing our connection to our email server
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email,
            msg=message)
    print("Email sent!")


while True:
    # Checks time and runs program at 9:00 daily
    date_time = datetime.datetime.now()
    time_now = date_time.strftime("%H:%M")
    if time_now == "17:42":
        product_details = get_product_details(TARGET)
        title = product_details.split("=>")[0]
        price = product_details.split("=>")[1]
        send_email(title, price)

        time.sleep(60)