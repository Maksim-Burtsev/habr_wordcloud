import re
import numpy as np

from nltk import word_tokenize
from gensim import corpora, models
from gensim.utils import simple_preprocess
from stop_words import get_stop_words

from config import ALPHABET
from services import _get_article_text, _create_wordcloud


def _clean_text(filename: str):
    """Очищает текст от лишних символов"""

    text = _get_article_text(filename)

    res = re.sub(r'<[^>]*\>', '', text).strip()
    res = re.sub(r'[0-9]+', '', res)

    s = ''
    for i in res:
        if i not in ALPHABET:
            s += i
    res = ''.join(s)

    res = re.sub(r' +', ' ', res)

    return res


def _tokinize(text: str) -> list:
    """Разбивает текст на токены"""

    tokenized = []
    for sentence in text.split('.'):
        tokenized.append(simple_preprocess(sentence, deacc=True))

    return tokenized


def _get_words_weights(bow_corpus, my_dictionary) -> list:
    """Рассчитывает вес слов в тексте при помощи модели"""

    tfIdf = models.TfidfModel(bow_corpus, smartirs='ntc')

    word_weights = []
    for doc in tfIdf[bow_corpus]:
        for id, freq in doc:
            word_weights.append(
                [my_dictionary[id], np.around(freq, decimals=3)])

    word_weights = sorted(word_weights, key=lambda para: para[1], reverse=True)
    # print(word_weights)

    return word_weights


def _get_clean_weights(word_weights):
    """Приводит слова к начальной форме и убирает из списка слов дубликаты"""

    words = ' '.join([i[0] for i in word_weights])
    text_tokens = word_tokenize(words)
    eng_words = _get_eng_words(text_tokens)

    for i in range(len(word_weights)):
        word_weights[i][0] = text_tokens[i]

    clean_weights = {}

    for i in word_weights:
        if i[0] not in clean_weights.keys() and i[0] not in eng_words:
            clean_weights[i[0]] = i[1]
    # print(clean_weights)
    return clean_weights


def _get_eng_words(text_tokens):
    """
    Достаёт английские слова из текста
    """
    eng_words = []
    for word in text_tokens:
        for letter in word:
            if letter in ALPHABET:
                eng_words.append(word)
                break

    return eng_words


def word_value_cloud_main(filename: str):

    text = _clean_text(filename)
    tokenized = _tokinize(text)

    my_dictionary = corpora.Dictionary(tokenized)
    bow_corpus = [my_dictionary.doc2bow(
        doc, allow_update=True) for doc in tokenized]

    word_weights = _get_words_weights(bow_corpus, my_dictionary)
    clean_weights = _get_clean_weights(word_weights)

    # print(clean_weights)

    text_raw = ''.join([(str(i)+' ')*int(clean_weights[i]*10)
                       for i in clean_weights])

    russian_stopwords = get_stop_words('russian')

    filename = f'{filename}_val'
    _create_wordcloud(russian_stopwords, text_raw, filename)


if __name__ == '__main__':
    word_value_cloud_main('594633')
