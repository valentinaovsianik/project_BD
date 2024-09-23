import json


class FileManager:
    """Класс для работы с файлами JSON."""

    @staticmethod
    def save_to_file(filename, data):
        """Сохраняет данные в файл."""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"Данные успешно сохранены в {filename}")
        except Exception as e:
            print(f"Ошибка при сохранении данных в файл {filename}: {e}")

    @staticmethod
    def load_from_file(filename):
        """Загружает данные из файла."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"Данные успешно загружены из {filename}")
            return data
        except FileNotFoundError:
            print(f"Файл {filename} не найден.")
        except json.JSONDecodeError:
            print(f"Ошибка при чтении файла {filename}: некорректный формат JSON.")
        except Exception as e:
            print(f"Ошибка при загрузке данных из файла {filename}: {e}")
