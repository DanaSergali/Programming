import sqlite3
import os
import re


# New (empty) DB generator
def create_database(db_name=''):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    c.execute("DROP TABLE IF EXISTS articles")
    c.execute("CREATE TABLE IF NOT EXISTS articles(title STRING, "
              "author STRING, date DATE, plain TEXT, mystem_plain "
              "TEXT, url STRING)")

    connection.commit()
    connection.close()


# For DB filling by data from articles
# at '/static/newspaper'
def add_articles():
    authorTag = '@au '
    titleTag = '@ti '
    dateTag = '@da '
    urlTag = '@url '
    regTag = re.compile('@.*?\n', re.DOTALL)
    regSpace = re.compile(r'\s{2,}', re.DOTALL)
    mystem_plain_path = 'static/newspaper/mystem-plain'
    plain_path = 'static/newspaper/plain'

    connection = sqlite3.connect('newspaper.db')
    c = connection.cursor()

    listY = os.listdir(plain_path)
    for dir_year in listY:
        plain_year_path = '%s/%s' % (plain_path, dir_year)
        if not os.path.isdir(plain_year_path):
            continue

        listM = os.listdir(plain_year_path)

        for dir_month in listM:
            plain_month_path = '%s/%s' % (plain_year_path, dir_month)
            if not os.path.isdir(plain_month_path):
                continue

            listF = os.listdir(plain_month_path)

            for _file in listF:
                file_path = '%s/%s' % (plain_month_path, _file)

                mystem_text_to_db = ''
                text_to_db = ''
                author = ''
                title = ''
                date = ''
                url = ''

                with open(file_path, 'r') as myfile:
                    index = 0
                    text = myfile.read().split('\n')
                    while index < len(text):
                        text[index] = regSpace.sub(' ', text[index])
                        index += 1
                    while True:
                        if '' in text:
                            text.remove('')
                        else:
                            if ' ' in text:
                                text.remove(' ')
                            else:
                                break

                    for t in text:
                        if authorTag in t:
                            author = t.replace(authorTag, '')
                            continue
                        if titleTag in t:
                            title = t.replace(titleTag, '')
                            continue
                        if dateTag in t:
                            date = t.replace(dateTag, '')
                            continue
                        if urlTag in t:
                            url = t.replace(urlTag, '')
                            continue
                        text_to_db += '%s\n' % (t)

                    text_to_db = regTag.sub('', text_to_db)

                mystem_file_path = '%s/%s/%s/%s' % (mystem_plain_path,
                                                    dir_year, dir_month, _file)

                with open(mystem_file_path, 'r') as myfile:
                    mystem_text_check = myfile.read().split(' ')
                    prev_word = ''
                    index = 0
                    to_delete = len(title.split(' ')) + len(
                        author.split(' ')) + 3
                    for word in mystem_text_check:
                        word = word.replace('?', '')
                        word = word.replace('!', '')
                        word = word.replace(',', '')
                        word = word.replace('.', '')
                        word = word.replace(':', '')
                        word = word.replace(';', '')
                        word = word.replace('?', '')
                        if not word == prev_word:
                            prev_word = word
                            if index < to_delete:
                                print('word to delete: %s' % (word))
                                index += 1
                                continue
                            mystem_text_to_db += '%s ' % (word)

                c.execute(
                    "INSERT INTO articles VALUES (?,?,?,?,?,?)",
                    (title, author, date, text_to_db, mystem_text_to_db, url))

    connection.commit()
    connection.close()


def find_articles(words):
    result = []
    connection = sqlite3.connect('newspaper.db')
    c = connection.cursor()

    for row in c.execute("SELECT * FROM articles"):
        check = False
        mystem_plain = row[4].replace('\n', ' ')
        orig_plain = row[3]
        for word in words:
            if check is True:
                break
            index = 0
            for test_word in mystem_plain.split(' '):
                index += 1
                if word == test_word:
                    check = True
                    plain_text = '...'
                    min = 0
                    max = len(orig_plain.split(' ')) - 1
                    if index > 50:
                        min = index - 50
                    if len(orig_plain.split(' ')) - index > 50:
                        max = index + 50
                    for pW in orig_plain.split(' ')[min: max]:
                        plain_text += '%s ' % (pW)

                    result.append(
                        {
                            'title': row[0],
                            'author': row[1],
                            'date': row[2],
                            'plain': plain_text,
                            'url': row[5]
                        }
                    )
                    break

    return result
