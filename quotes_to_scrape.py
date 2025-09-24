from time import sleep

from requests import Session
from bs4 import BeautifulSoup
import xlsxwriter

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

# создаем Excel-файл
workbook = xlsxwriter.Workbook("quotes.xlsx")
worksheet = workbook.add_worksheet("Quotes")

# Заголовки столбцов
worksheet.write(0, 0, "№")
worksheet.write(0, 1, "Цитата")
worksheet.write(0, 2, "Автор")


page = 1  # Начальная страница
row = 1  # Начинаем со второй строки, т.к. первая — заголовки

while True:
    # Парсинг страницы
    url = f"https://quotes.toscrape.com/page/{page}/"
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    quotes_div = soup.find_all("div", class_="quote")

    if len(quotes_div) == 0:  # Если на странице больше нет цитат
        print(f"Завершение на странице {page}, так как цитаты закончились.")
        break

    for num, item in enumerate(quotes_div, 1):
        sleep(1)
        quote = item.find("span", class_="text").text
        author = item.find("small", class_="author").text
        index = (page - 1) * 10 + num

        print(f"{index}. {quote}\n{author}")

        # Запись в Excel
        worksheet.write(row, 0, index)
        worksheet.write(row, 1, quote)
        worksheet.write(row, 2, author)
        row += 1

    page += 1  # Переход на следующую страницу


# сохраняем файл
workbook.close()
print("Данные успешно сохранены в quotes.xlsx")

