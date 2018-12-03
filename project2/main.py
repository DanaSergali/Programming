from flask import Flask
from flask import render_template, url_for, request, redirect, jsonify
import csv
import os.path
import io

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
wordsbook = {}
currentuser = {}
fname = 'data.csv'
correctAnswers = {'q1': 'yes', 'q2': 'yes', 'q3': 'no', 'q4': 'yes',
                  'q5': 'no', 'q6': 'yes', 'q7': 'yes', 'q8': 'no',
                  'q9': 'no', 'q10': 'yes', 'q11': 'yes', 'q12': 'no',
                  'q13': 'no', 'q14': 'yes'}


@app.route('/')
def index():
    if request.args:
        if 'age' in request.args:
            currentuser['age'] = request.args['age']
            currentuser['gender'] = request.args['gender']
            currentuser['edu'] = request.args['edu']
            currentuser['city'] = request.args['city']
            currentuser['native'] = request.args['native']
            return render_template('index.html', age=currentuser['age'])
        else:
            answers = currentuser
            fieldnames = ['age', 'gender', 'edu', 'city', 'native']
            for i in range(1, 15):
                i_s = 'q%d' % i
                if request.args[i_s] == correctAnswers[i_s]:
                    answers[i_s] = 'correct'
                else:
                    answers[i_s] = 'wrong'
                fieldnames.append(i_s)

            check = os.path.isfile(fname)
            with open(fname, "a", newline='', encoding='utf8') as csv_file:
                writer = csv.DictWriter(
                    csv_file, delimiter='\t', fieldnames=fieldnames)
                if not check:
                    writer.writeheader()
                writer.writerow(answers)

            return render_template('index.html', end=True, answers=answers)
    else:
        currentuser.clear()
        return render_template('index.html')


@app.route('/stats')
def stats():
    age_pie = {'Меньше 18': 0, '18-25': 0,
               '26-40': 0, '41-60': 0, 'Больше 60': 0}
    gender_pie = {'М': 0, 'Ж': 0}
    edu_pie = {'Среднее': 0, 'Среднее специальное': 0,
               'Неоконченное высшее': 0, 'Высшее': 0}
    city = []
    lang = []
    all = 0
    mistakes = 0
    corrects = 0
    if os.path.isfile(fname):
        with open(fname, "r", encoding='utf8') as csv_file:
            reader = csv.DictReader(
                csv_file, delimiter='\t')
            for row in reader:
                city.append(row['city'])
                lang.append(row['native'])
                all += 1
                for ages in age_pie:
                    if row['age'] == ages:
                        age_pie[ages] += 1
                for gen in gender_pie:
                    if row['gender'] == gen:
                        gender_pie[gen] += 1
                for edu in edu_pie:
                    if row['edu'] == edu:
                        edu_pie[edu] += 1
                for q in correctAnswers:
                    if row[q] == 'wrong':
                        mistakes += 1
                    else:
                        corrects += 1
    return render_template('stats.html', all=all, mistakes=mistakes,
                           corrects=corrects, age_pie=age_pie,
                           gender_pie=gender_pie, edu_pie=edu_pie,
                           city=city, lang=lang)


@app.route('/json')
def json():
    json_r = []
    if os.path.isfile(fname):
        with open(fname, "r", encoding='utf8') as csv_file:
            reader = csv.DictReader(
                csv_file, delimiter='\t')
            for row in reader:
                json_r.append(row)
    return jsonify(json_r), 200, {'Content-Type': 'text/css; charset=utf-8'}


@app.route('/search')
def search():
    if request.args:
        return redirect(url_for('result',
                                percentage=request.args['percentage'],
                                gender=request.args['gender']))
    else:
        return render_template('search.html')


@app.route('/result')
def result():
    total_q = 14
    result = []
    per = int(request.args['percentage'])
    gen = request.args['gender']
    if os.path.isfile(fname):
        with open(fname, "r", encoding='utf8') as csv_file:
            reader = csv.DictReader(
                csv_file, delimiter='\t')
            for row in reader:
                if gen == 'both' or gen == row['gender']:
                    counter = 0
                    for key in row:
                        if 'q' not in key:
                            continue
                        if row[key] == 'correct':
                            counter += 1
                    p = (100 * counter) / total_q
                    if p >= per:
                        result.append(row)
    if gen == 'both':
        gen = 'Любой'
    return render_template('result.html', p=per, g=gen, result=result)


if __name__ == '__main__':
    app.run(debug=True)
