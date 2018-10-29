from csv_writer import save_to_csv
from dirs import create_dir_by_date

import urllib.request
import time
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'     # агент для допуска на сайт
visited_pages = []                                          # уже посещенные страницы
pages_to_visit = []                                         # общий список найденных страниц для посещения


# функция для сохранения статьи и метаданных
def save_article(text, source):
    save_to_csv('metadata.csv', 'blah blah', text, source)
    return


def download_page(common_url, page_url, pages_limit):
    try:
        req = urllib.request.Request(page_url, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('windows-1251')
    except:
        print('Error at page ', page_url)
        return

    visited_pages.append(page_url)

    save_article(text, page_url)

    soup = BeautifulSoup(text, 'html.parser')

    # постепенное добавление страниц по принципу краулеров с вычетом повторяющихся страниц
    if pages_limit > len(pages_to_visit):
        for post in soup.find_all('div', {'class': 'also-read'}):
            for a_s in post.find_all('a', {'class': 'alsr-item'}):
                href = a_s.get('href')

                if common_url not in href:
                    href = common_url + href
                print(href)
                if href not in pages_to_visit:
                    pages_to_visit.append(href)

            print('--' * 10)
            print(len(pages_to_visit))


def connect(common_url, pages_limit):
    req = urllib.request.Request(common_url, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        main_page = response.read().decode('windows-1251')

    soup = BeautifulSoup(main_page, 'html.parser')

    for post in soup.find_all('div', {'class': 'city-news-item-name'}):
        print(post)
        link = post.find('a')
        print(link)
        if link:
            href = link.get('href')
            if common_url not in href:
                href = common_url + href
            if pages_limit > len(pages_to_visit):
                if href not in pages_to_visit:
                    pages_to_visit.append(href)
            else:
                break

    print(len(pages_to_visit))
    for p in pages_to_visit:
        print(p)

    for p in pages_to_visit:
        print(p)
        download_page(common_url, p, pages_limit)
        time.sleep(2)
