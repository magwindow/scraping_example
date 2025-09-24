from requests import Session
from bs4 import BeautifulSoup

headers = {"User-Agent": "CrookedHands/2.0 (EVM x8), CurlyFingers20/1;p"}

session = Session()

session.get("https://quotes.toscrape.com/", headers=headers)
response = session.get("https://quotes.toscrape.com/login", headers=headers)

soup = BeautifulSoup(response.text, "lxml")

# Получаем csrf_token
token = soup.find("form").find("input").get("value")

print(token)