from csv_writer import save_to_csv
from dirs import create_dir_by_date

import urllib.request
import time
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'     # агент для допуска на сайт
visited_pages = []                                          # уже посещенные страницы
pages_to_visit = []                                         # общий список найденных страниц для посещения


# для создания описательного колонтитула в оригинальной статье
def create_meta_original(meta):
    author = "@au %s" % (meta[1])
    title = "@ti %s" % (meta[2])
    date = "@da %s" % (meta[3])
    topic = "@topic %s" % (meta[5])
    url = "@url %s" % (meta[10])

    return [author, title, date, topic, url]


def fetch_text(soup):
    body = soup.find('div', {'class': 'news-text'})

    lines = body.find_all('p', {'class': 'western'})

    text = []

    for l in lines:
        text.append(l.get_text())

    return text


# функция для сохранения статьи и метаданных
def save_article(text, source):
    soup = BeautifulSoup(text, 'html.parser')

    main_info = soup.find('div', {'class': 'news-info'})  # главная информация о статье
    text_div = main_info.get_text().split('\n')
    created = text_div[3].replace("\t", "")[:10].split('.')

    create_dir_by_date(created[2], created[1])

    article_path_dir = "newspaper/plain/%s/%s" % (created[2], created[1])
    article_path = "%s/article_%d.txt" % (article_path_dir, len(visited_pages))

    meta = save_to_csv('metadata.csv', article_path, text, source)

    pre = create_meta_original(meta)

    text = fetch_text(soup)

    for t in text:
        print(t)

    out_f = open(article_path, 'w')
    for line in pre:
        out_f.write(line)
        out_f.write('\n')

    out_f.write('\n')

    for line in text:
        out_f.write(line)
        out_f.write('\n')

    out_f.close()


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
