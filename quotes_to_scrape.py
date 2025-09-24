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

# Начальная страница
page = 1

while True:
    # Парсинг страницы
    url = f'https://quotes.toscrape.com/page/{page}/'
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes_div = soup.find_all('div', class_='quote')

    if len(quotes_div) == 0:  # Если на странице больше нет цитат
        print(f'Завершение на странице {page}, так как цитаты закончились.')
        break

    for num, item in enumerate(quotes_div, 1):
        sleep(1)
        quote = item.find('span', class_='text').text
        author = item.find('small', class_='author').text
        print(f'{(page-1) * 10 + num}. {quote}\n{author}')

    page += 1  # Переход на следующую страницу
