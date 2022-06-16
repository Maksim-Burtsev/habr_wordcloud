from loguru import logger

from parser import get_clean_page_text
from word_value import word_value_cloud_main
from word_frequency import word_freq_cloud_main
from services import is_link_valid, _get_article_id


def make_word_cloud(link: str) -> None | str:
    """Создаёт облако слов на основе статьи и сохраняет его в текущую директорию с расширением .png"""

    if is_link_valid(link):
        filename = _get_article_id(link)
        try:
            get_clean_page_text(link, filename)
            
        except Exception as e:
            logger.error(e)
        else:
            logger.debug(f'Успешный парсинг статьи {link}')
            word_value_cloud_main(filename)
            word_freq_cloud_main(filename)
            logger.debug(f'Успешное создание облаков слов')
        return

    logger.info('Ссылка не валидная')


if __name__ == '__main__':
    # make_word_cloud('https://habr.com/ru/post/664882')
    make_word_cloud('https://habr.com/ru/company/tuturu/blog/669728/')
