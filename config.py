from configparser import ConfigParser

HH_API_URL = "https://api.hh.ru/employers"
HH_API_MAX_PAGES = 1
HH_API_MAX_PER_PAGE = 100

HH_ORG_LIST=[
            "78638",   # Т-Банк
            "3529",    # СБЕР
            "2324020", # Точка
            "2173850", # Аэрофлот Техникс
            "5008932", # Яндекс Практикум
            "816144",  # ВкусВилл
            "3757",    # Ингосстрах Банк
            "1122462", # Skyeng
            "2748",    # Ростелеком
            "2180",    # Ozon
        ]


def get_config_db(filename='database.ini', section='postgresql'):
    """
	Прочитать конфигурацию базы данных
    """
    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db
