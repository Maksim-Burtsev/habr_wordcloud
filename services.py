import random

from wordcloud import WordCloud

from config import COLORMAPS


def _get_article_text(filename: str) -> str:
    """
    Достаёт текст из файла
    """

    with open(f'articles/{filename}.txt', encoding='utf-8') as f:
        text = f.read()

    return text


def is_link_valid(link: str) -> bool:
    """Проверяет ссылку на корректность"""

    correct_link_parts = ['https:', 'habr.com', 'ru']

    link = link.split('/')

    while '' in link:
        link.remove('')

    for part in correct_link_parts:
        if part not in link:
            return False

    return link[-1].isdigit() and len(link[-1]) == 6


def _create_wordcloud(russian_stopwords, text_raw, filename):
    """Создаёт облако слов и сохраняет его в /clouds"""

    colormap = random.choice(COLORMAPS)
    wordcloud = WordCloud(
        width=1280,
        height=720,
        random_state=1,
        background_color=None,
        margin=20,
        colormap=colormap,
        collocations=False,
        stopwords=russian_stopwords,
    ).generate(text_raw)

    wordcloud.to_file(f'clouds/{filename}.png')


def _get_article_id(link: str) -> str:
    """
    Достатёт из ссылки на статью её id

    'https://habr.com/ru/news/t/670564/' -> '670564'
    """

    return str([i for i in link.split('/') if i][-1])


if __name__ == '__main__':
    _get_article_id('https://habr.com/ru/news/t/670564/')