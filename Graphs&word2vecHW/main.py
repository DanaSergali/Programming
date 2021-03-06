from flask import Flask
from flask import render_template, url_for, request, redirect, jsonify
import re
import os
import datetime
import random
import gensim
import logging
import pandas as pd
import progressbar
import urllib.request
from gensim.models import word2vec
import networkx as nx
from networkx.algorithms import community
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

# Пояснения:
# При стартовой загрузке происводится работа со словами из
# семантического поля "Искусство". На странице "Расчет"
# можно провести расчеты для произвольного слова (сущ.)

# Семантическое поле "Искусство"
# Узлы-слова:
nodes_base = ['творчество', 'живопись', 'художник',
              'музыка', 'музей', 'картина', 'красота',
              'кино', 'архитектура', 'краска', 'арт',
              'рисунок', 'фотография', 'поэзия', 'статуя',
              'любовь', 'танец', 'мастерство']
postfix = '_S'

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

pbar = None
model = None

m = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'


# вспомогательная функция для отслеживания состояния скачивания
def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


# функция для скачивания модели с сайта rusvectores
def dowload_model(name):
    print('Downloading...')
    urllib.request.urlretrieve(
        "http://rusvectores.org/static/models"
        "/rusvectores2/ruscorpora_mystem_cbow_300_2_2015.bin.gz",
        m, show_progress)
    print('Download Completed!')


# загружаем модель
dowload_model(m)

if m.endswith('.vec.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(
        m, binary=False)
elif m.endswith('.bin.gz'):
    model = gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
else:
    model = gensim.models.KeyedVectors.load(m)


@app.route('/')
def index():
    random.seed()
    id = random.randint(0, len(nodes_base) - 1)
    word = nodes_base[id]

    return redirect(url_for('result',
                            word=word))


@app.route('/new_node')
def new_node():
    if request.args:
        return redirect(url_for('result',
                                word=request.args['requestText']))
    else:
        return render_template('new_node.html')


@app.route('/result')
def result():
    word = request.args['word']
    wordInModel = word + postfix
    wordExists = True
    G = nx.Graph()
    gIndex = 1

    if wordInModel in model:
        G.add_node(word)

        for i in model.most_similar(positive=[wordInModel], topn=100):
            similar = i[0]
            # фильтр для отбора существительных
            if similar.split('_')[1] != 'S':
                continue
            w = similar.split('_')[0]
            coeff = i[1]

            if coeff < 0.5:
                break

            gIndex += 1
            G.add_node(w)
            G.add_edge(word, w)

            gIndexS = gIndex
            for j in model.most_similar(positive=[similar], topn=100):
                similarJ = j[0]
                wS = similarJ.split('_')[0]
                coeffS = j[1]

                if coeffS < 0.5:
                    break

                gIndexS += 1
                G.add_node(wS)
                G.add_edge(w, wS)
                for node in G.nodes():
                    n = node + '_S'
                    if (n in model) & (similarJ in model):
                        if model.similarity(n, similarJ) >= 0.5:
                            G.add_edge(node, wS)

            gIndex = gIndexS

        pos = nx.spring_layout(G, k=4, scale=1500, iterations=50)
        nx.draw_networkx_nodes(G, pos, node_color='red', node_size=20, width=3)
        nx.draw_networkx_edges(G, pos, edge_color='green')
        nx.draw_networkx_labels(G, pos, font_size=8, font_family='Verdana')
        plt.axis('off')
        plt.ioff()
        if not os.path.exists('static'):
            os.mkdir('static')
        else:
            if os.path.exists('static/graph.png'):
                os.remove('static/graph.png')

        plt.savefig('static/graph.png')
        plt.close()

        nodesN = G.number_of_nodes()
        edgesN = G.number_of_edges()
        density = nx.density(G)
        radius = nx.radius(G)
        diameter = nx.diameter(G)
        ac = nx.average_clustering(G)
        if G.number_of_nodes() > 1:
            dpcc = nx.degree_pearson_correlation_coefficient(G)
        else:
            dpcc = '-'

        deg = nx.degree_centrality(G)
        degC = sorted(deg, key=deg.get, reverse=True)[0]
        close = nx.closeness_centrality(G)
        closeC = sorted(close, key=close.get, reverse=True)[0]
        between = nx.betweenness_centrality(G)
        betweenC = sorted(between, key=between.get, reverse=True)[0]
        try:
            eigen = nx.eigenvector_centrality(G)
            eigenC = sorted(eigen, key=eigen.get, reverse=True)[0]
        except:
            print('Could not calculate eigenvector_centrality')
            eigenC = '-'

        dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        return render_template('result.html', word=word,
                               isWordExists=wordExists,
                               nodesN=nodesN, edgesN=edgesN, density=density,
                               radius=radius, diameter=diameter,
                               dpcc=dpcc, ac=ac, deg=degC, close=closeC,
                               between=betweenC, eigen=eigenC, dt=dt)
    else:
        wordExists = False
        return render_template('result.html', word=word,
                               isWordExists=wordExists)


if __name__ == '__main__':
    app.run(debug=True)
