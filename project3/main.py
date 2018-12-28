from flask import Flask
from flask import render_template, url_for, request, redirect
from pymystem3 import Mystem
import os
import os.path
import articles

app = Flask(__name__)
db_name = 'newspaper.db'


@app.route('/')
def index():
    if request.args:
        return redirect(url_for('result',
                                requestText=request.args['requestText']))
    else:
        return render_template('index.html', requestText='')


@app.route('/result')
def result():
    if not request.args:
        return render_template('error.html')

    m = Mystem(entire_input=False)
    srch_phrase = request.args['requestText']

    lemmas = m.lemmatize(srch_phrase)

    art_list = articles.find_articles(lemmas)

    return render_template('result.html', requestText=srch_phrase,
                           art_list=art_list)


# In case the database does not exist, but the "newspaper"
# block placed in "static" folder
#
# This page generates new DB: "newspaper.db" and
# adds all articles in it
@app.route('/createdb')
def createdb():
    if os.path.isfile(db_name):
        articles.create_database(db_name)

    articles.add_articles()
    return render_template('createdb.html')


if __name__ == '__main__':
    app.run(debug=True)
