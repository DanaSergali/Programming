import urllib.request
import json
import base64

# Впишите свой токен сюда
token = ""

def get_json_by_url(url):
    url += '?access_token={}'.format(token)
    f = urllib.request.urlopen(url)
    myfile = f.read()
    return json.loads(myfile)

def get_username(users):
    if len(users) == 0:
        print('Список пользователей пуст.')
    print('Введите никнейм:')
    username = input()
    exit = False
    if username not in users:
        print('Такого имени нет.')
        return ''
    return username

def get_user_url(username):
    return 'https://api.github.com/users/{}'.format(username)

def get_user_repos(username):
    url = get_user_url(username) + '/repos'
    return get_json_by_url(url)

def print_user_info(users):
    if len(users) == 0:
        print('Список пользователей пуст.')
    username = get_username(users)
    got_username = (username != '')
    if not got_username:
        return
    print('\nВы выбрали {}.\n'.format(username))
    repos = get_user_repos(username)
    print('Его репозитории:\n')
    for repo in repos:
        print('{} - {}'.format(repo['name'], repo['description']), end='')
        if repo != repos[-1]:
            print(',')
        else:
            print('.\n')
    return

def get_user_languages(username):
    repos = get_user_repos(username)
    lang_repos = dict()
    for repo in repos:
        lang_url = repo['languages_url']
        
        langs = get_json_by_url(lang_url).keys()    
        for lang in langs:
            print('.', end='')
            if not lang in lang_repos.keys():
                lang_repos[lang] = [repo['name']]
            else:
                lang_repos[lang].append(repo['name'])
            
    return lang_repos.keys(), lang_repos.values()

def print_user_languages(users):
    if len(users) == 0:
        print('Список пользователей пуст.')
    username = get_username(users)
    got_username = (username != '')
    if not got_username:
        return
    languages, repos = get_user_languages(username)
    languages = list(languages)
    repos = list(repos)
    print('\n{} использует {}'.format(username, ', '.join(languages)), end='.\n')
    print()
    for i in range(len(languages)):
        print('\n{} используется в {} репозиториях: {}.\n'.format(languages[i], len(repos[i]), ', '.join(repos[i])))
    print()
    return

def get_repos_number(username):
    url = get_user_url(username)
    number = get_json_by_url(url)['public_repos']
    return number

def print_biggest_owner(users):
    if len(users) == 0:
        print('Список пользователей пуст.')
    max_repos = 0
    owner = ''
    for user in users:
        print('.', end='')
        repos_number = get_repos_number(user)
        if (repos_number > max_repos):
            max_repos = repos_number
            owner = user
    print('\nБольше всего ({}) репозиториев у {}.\n'.format(max_repos, owner))
    return


def print_most_popular_language(users):
    languages_popularity = dict()
    for user in users:
        print('.', end='')
        languages, repos = get_user_languages(user)
        for lang in languages:
            if lang in languages_popularity.keys():
                languages_popularity[lang] += 1
            else:
                languages_popularity[lang] = 1
    max_popularity = max(languages_popularity.values())
    most_pop_languages = []
    for lang in languages_popularity.keys():
        if languages_popularity[lang] == max_popularity:
            most_pop_languages.append(lang)
    plural = len(most_pop_languages) > 1
    if plural:
        print('\nСамые популярные языки: {}.'.format(', '.join(most_pop_languages)))
    else:
        print('\nСамый популярный язык: {}.'.format(most_pop_languages[0]))
    print()
    return

def get_user_followers_number(username):
    url = get_user_url(username)
    number = get_json_by_url(url)['followers']
    return number

def print_most_popular_githuber(users):
    max_followers = 0
    most_pop_githuber = ''
    for user in users:
        print('.', end='')
        n_followers = get_user_followers_number(user)
        if n_followers > max_followers:
            max_followers = n_followers
            most_pop_githuber = user
    print('\nБольше всего ({}) подписчиков у {}.'.format(max_followers, most_pop_githuber))
    print()
    return

def print_menu():
    print('\nВыберите один из пунктов и введите соответствующую цифру:\n')
    print('1. Вывести информацию о репозиториях конкретного пользователя.')
    print('2. Вывести информацию о языках конкретного пользователя.')
    print('3. Вывести пользователя с наибольшим количеством репозиториев.')
    print('4. Вывести пользователя с наибольшим количеством подписчиков.')
    print('5. Вывести самый популярный язык.')
    print('0. Выход.')
    print()

def main(users):
    while True:
        print_menu()
        
        option = input()
        correct_option = (option.isdigit() and (0 <= int(option) <= 5))
        while not correct_option:
            print('Неверный ввод. Введите число от 0 до 5.')
            option = input()
            correct_option = (option.isdigit() and (0 <= int(option) <= 5))
        option = int(option)
        
        print('\nЗагружаем..', end='')
        if option == 1:
            print_user_info(users)
        elif option == 2:
            print_user_languages(users)
        elif option == 3:
            print_biggest_owner(users)
        elif option == 4:
            print_most_popular_githuber(users)
        elif option == 5:
            print_most_popular_language(users)
        else:
            return
    
def parse_users_string(users_str):
    users = users_str.split(', ')
    return users
    
if __name__ == "__main__":
    users = parse_users_string('elmiram, maryszmary, lizaku, nevmenandr, ancatmara, roctbb, akutuzov, agricolamz, lehkost')
    main(users)
