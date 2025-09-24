from time import sleep

from requests import Session
from bs4 import BeautifulSoup

# предоставляем информацию о нас, сайту
headers = {"User-Agent": "CrookedHands/2.0 (EVM x8), CurlyFingers20/1;p"}

# POST - авторизация
session = Session()
session.get("https://quotes.toscrape.com/", headers=headers)
response = session.get("https://quotes.toscrape.com/login", headers=headers)
soup = BeautifulSoup(response.text, "lxml")

token = soup.find("form").find("input").get("value")  # Получаем csrf_token
data = {"csrf_token": token, "username": "anonim", "password": "anonim"}

# Авторизуемся на сайте
session.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects=True)

# Парсинг страницы
url = f'https://quotes.toscrape.com/page/1/'
response = session.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
quotes_div = soup.find_all('div', class_='quote')

for num, item in enumerate(quotes_div, 1):
    sleep(1)
    quote = item.find('span', class_='text').text
    author = item.find('small', class_='author').text
    print(f'{num}. {quote}\n{author}')
