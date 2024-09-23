from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    """Возвращает параметры для подключения к базе данных из конфигурационного файла."""
    parser = ConfigParser()
    parser.read(filename)

    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f"Раздел {section} не найден в {filename}")

    return db_params
