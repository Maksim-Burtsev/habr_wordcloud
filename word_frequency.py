import re
import string

import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from stop_words import get_stop_words

from config import ALPHABET
from services import _get_article_text, _create_wordcloud


def get_cleaned_text(filename: str) -> str:
    """Достаёт текст из файла и очищает его от служебных и лишних символов"""

    text = _get_article_text(filename).lower()

    special_chars = string.punctuation + '\n\xa0«»\t—…•№'

    text = ''.join([i for i in text if i not in special_chars])

    new_text = ''
    for i in text:
        if i not in ALPHABET:
            new_text += i

    text = re.sub(r' +', ' ', new_text)

    return text


def _make_raw_text(file_text, russian_stopwords) -> str:
    """Удаление стоп-слов из текста"""

    text_tokens = word_tokenize(file_text)
    text = nltk.Text(text_tokens)
    fdist = FreqDist(text)

    for word in russian_stopwords:
        fdist.pop(word, None)
    text_raw = ''
    for i,_ in sorted(fdist.items(), key=lambda x: x[1], reverse=True):
        text_raw += f'{i} '
    print(text_raw)
    return text_raw


def word_freq_cloud_main(filename: str):

    russian_stopwords = stopwords.words('russian') + get_stop_words('russian')

    text = get_cleaned_text(filename=filename)
    text_raw = _make_raw_text(text, russian_stopwords)

    filename = f'{filename}_freq'
    _create_wordcloud(russian_stopwords, text_raw, filename)


if __name__ == '__main__':
    # https://habr.com/ru/company/tuturu/blog/669728/
    word_freq_cloud_main('669728')
