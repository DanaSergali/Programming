import csv
from bs4 import BeautifulSoup


def parse_soup(article_path, text, source):
    soup = BeautifulSoup(text, 'html.parser')

    main_info = soup.find('div', {'class': 'news-info'})  # главная информация о статье
    header = main_info.find('strong').get_text()
    header = header.replace("\t", "")
    header = header.replace("\n", "")

    author = main_info.find('a').get_text()
    author = author.replace(" ", "")

    text_div = main_info.get_text().split('\n')
    created = text_div[3].replace("\t", "")[:10]

    audience_age_div = soup.find('div', {'class': 'header-paper'})
    audience_age = audience_age_div.find('img').get('title')
    audience_age = audience_age.replace('.jpg', '')

    publication = soup.find('div', {'class': 'title'}).get_text()

    year = created.split('.')
    publ_year = year[len(year) - 1]

    # topic и audience_level не получилось вытащить со страницы со статьей
    row = [article_path, author, header, created, "публицистика", "None", "нейтральный", audience_age, "None",
           "районная", source, publication, publ_year, "газета", "Россия", "ru"]

    return row


def save_to_csv(csv_path, article_path, text, source):
    row = parse_soup(article_path, text, source)

    with open(csv_path, "a", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='\t')
        writer.writerow(row)

    return row
