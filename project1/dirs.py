import os
import shutil


# функция создает первоначальную разметку папок при старте
def init_dirs():
    shutil.rmtree('newspaper', ignore_errors=True)
    os.makedirs('newspaper/plain')
    os.makedirs('newspaper/mystem-xml')
    os.makedirs('newspaper/mystem-plain')
    return


# создание папок по дате для статьи и ее анализа
def create_dir_by_date(year, month):
    year_str = year.str()
    month_str = month.str()
    os.makedirs('newspaper/plain/%s/%s' % (year_str, month_str))
    os.makedirs('newspaper/mystem-xml/%s/%s' % (year_str, month_str))
    os.makedirs('newspaper/mystem-plain/%s/%s' % (year_str, month_str))
