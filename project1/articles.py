from csv_writer import save_to_csv
from dirs import create_dir_by_date
import urllib.request
import time
from bs4 import BeautifulSoup

user_agent = 'Chrome/11.0 (Windows NT 6.1; Win64; x64)'     # агент для допуска на сайт
visited_pages = []                                          # уже посещенные страницы
pages_to_visit = []                                         # общий список найденных страниц для посещения
count_words = [0]                                           # примерный подсчет количества слов


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

    lines = body.find_all('p')

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

    meta = save_to_csv('newspaper/metadata.csv', article_path, text, source)

    pre = create_meta_original(meta)

    text = fetch_text(soup)

    # подсчет слов
    for lll in text:
        some_shit = lll.split()
        for sd in some_shit:
            if len(sd) > 1:
                count_words[0] += len(sd)

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


def add_local_pages(common_url, soup, pages_limit):
    city_news = soup.find('div', {'class': 'city-news'})
    aside = city_news.find('div', {'class': 'aside-block-link'})
    link = aside.find('a').get('href')
    link = common_url + link

    time.sleep(1)
    req = urllib.request.Request(link, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        main_page = response.read().decode('windows-1251')

    soup_c = BeautifulSoup(main_page, 'html.parser')

    for pg in range(25, 31):
        pager = soup_c.find('div', {'class': 'pager'})
        link_c = "%s%s%d" % (common_url, pager.find('a').get('href'), pg)

        time.sleep(1)
        req_city = urllib.request.Request(link_c, headers={'User-Agent': user_agent})
        with urllib.request.urlopen(req_city) as response:
            main_page_city = response.read().decode('windows-1251')

        soup_city = BeautifulSoup(main_page_city, 'html.parser')
        news_div = soup_city.find('div', {'class': 'news-content'})
        for blog in news_div.find_all('div', {'class': 'blogs-item'}):
            link_add = common_url + blog.find('a').get('href')
            if pages_limit > len(pages_to_visit):
                if link_add not in pages_to_visit:
                    pages_to_visit.append(link_add)
            else:
                break

    return


def connect(common_url, pages_limit):
    req = urllib.request.Request(common_url, headers={'User-Agent': user_agent})
    with urllib.request.urlopen(req) as response:
        main_page = response.read().decode('windows-1251')

    soup = BeautifulSoup(main_page, 'html.parser')

    for post in soup.find_all('div', {'class': 'city-news-item-name'}):
        link = post.find('a')
        if link:
            href = link.get('href')
            if common_url not in href:
                href = common_url + href
            if pages_limit > len(pages_to_visit):
                if href not in pages_to_visit:
                    pages_to_visit.append(href)
            else:
                break

    # добавление локальных новостей города
    add_local_pages(common_url, soup, pages_limit)

    for p in pages_to_visit:
        download_page(common_url, p, pages_limit)
        time.sleep(0.5)

    print(count_words)
