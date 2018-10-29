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
    plain = 'newspaper/plain/%s/%s' % (year, month)
    mystem_xml = 'newspaper/mystem-xml/%s/%s' % (year, month)
    mystem_plain = 'newspaper/mystem-plain/%s/%s' % (year, month)

    if not os.path.exists(plain):
        os.makedirs(plain)

    if not os.path.exists(mystem_xml):
        os.makedirs(mystem_xml)

    if not os.path.exists(mystem_plain):
        os.makedirs(mystem_plain)
