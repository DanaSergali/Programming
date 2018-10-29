import os


def mystem_my_file(file_path, year, month, file):
    f = file.replace(".txt", ".xml")
    xml_path = "newspaper/mystem-xml/%s/%s/%s" % (year, month, f)

    # mystem лежит в корне проекта, поэтому запускатся как "./mystem"
    os.system(r"./mystem -clisd --eng-gr --format xml %s %s" % (file_path, xml_path))

    return


def write_mystem_xml():
    home_path = 'newspaper/plain'

    list_y = os.listdir(home_path)  # dir is your directory path
    for dir_y in list_y:
        y_path = "%s/%s" % (home_path, dir_y)

        if os.path.isdir(y_path):
            list_m = os.listdir(y_path)

            for dir_m in list_m:
                m_path = "%s/%s" % (y_path, dir_m)

                if os.path.isdir(m_path):
                    list_f = os.listdir(m_path)

                    for file in list_f:
                        file_path = "%s/%s" % (m_path, file)
                        mystem_my_file(file_path, dir_y, dir_m, file)

    return
