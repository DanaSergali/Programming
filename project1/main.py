import articles
import dirs

common_url = 'http://www.zarpressa.ru'     # страница сайта
pages_limit = 5                   # количество статей для посещения

# инициализация структуры директории для сохранения всех статей и результатов анализов
dirs.init_dirs()

# сначала делается поиск и загрузка страниц со статьями
articles.connect(common_url, pages_limit)
