import re

from selenium import webdriver
from bs4 import BeautifulSoup

from config import DRIVER_PATH, ARTICLES_PATH


def _get_clean_text(html: str) -> str:
    """
    Очищает тест от тегов
    """

    article = _get_text_block(html)

    res = re.sub(r'<[^>]*\>', '', article).strip()
    res = re.sub(r' +', ' ', res)
    res = ' '.join(res.split()[:-1])

    return res

def _get_text_block(html:str):
    """
    Достаёт блок с текстом из html-страницы
    """

    soup = BeautifulSoup(html, 'lxml')

    article = soup.find('article')
    footer = article.find('div', {'class': 'tm-article-presenter__meta'})

    article = str(article).replace(str(footer), '')

    return article


def _get_page_html(url: str) -> str:
    """
    Прогружает веб-страницу и достатёт из неё html
    """

    browser = webdriver.Edge(executable_path=DRIVER_PATH)
    browser.get(url)

    return browser.page_source


def get_clean_page_text(link: str, filename: int):
    """
    Парсит страницу статьи и достаёт из неё чистый текст. 
    Результат записывается в файл с расширением .txt
    """

    page = _get_page_html(link)
    text = _get_clean_text(page)
    _write_text_in_file(text, filename)


def _write_text_in_file(text: str, filename: str) -> None:
    """
    Записывает текст в файл
    """
    with open(f'articles\{filename}.txt', 'w', encoding='utf-8') as f:
        f.write(text)