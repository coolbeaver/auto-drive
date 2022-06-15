import requests
from bs4 import BeautifulSoup


def pars_news():
    url = 'https://www.autonews.ru/'

    page = requests.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    allNews = soup.findAll('div', class_='l-base__col__33p')
    return allNews

