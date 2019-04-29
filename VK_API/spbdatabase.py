import sqlite3

db_name = 'vk_spb.db'


def create_database():
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    c.execute("DROP TABLE IF EXISTS posts")
    c.execute("DROP TABLE IF EXISTS comments")
    c.execute(
        """CREATE TABLE IF NOT EXISTS posts(
          id integer PRIMARY KEY,
          text_orig TEXT,
          text_lemm TEXT
          )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS comments(
          id integer PRIMARY KEY,
          post_id integer NOT NULL,
          text_orig TEXT,
          text_lemm TEXT,
          author_id integer NOT NULL,
          author_sex STRING,
          author_city STRING,
          author_age integer,
          FOREIGN KEY (post_id) REFERENCES posts (id)
          )"""
    )

    connection.commit()
    connection.close()


# Save 1 post to database
def add_post(post):
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    c.execute(
        "INSERT INTO posts VALUES (?, ?, ?)",
        (post['id'], post['text'], post['lemm'])
    )

    for comment in post['comments']:
        c.execute(
            "INSERT INTO comments VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (comment['id'], comment['post_id'],
             comment['text'], comment['lemm'],
             comment['user_id'], comment['user_sex'],
             comment['user_city'], comment['user_age'])
        )

    connection.commit()
    connection.close()


def getStopWords():
    f = open('stop_words', 'r', encoding='utf-8')
    swords = f.read()
    f.close()
    return swords.split(' ')
