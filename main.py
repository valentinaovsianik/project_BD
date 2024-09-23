from src.api_hh import HH
from src.db import DBManager
from src.file_module import FileManager


def main():
    """Функция взаимодействия с пользователем. Реализует интерфейс для работы с данными компаний и вакансий."""
    db_manager = DBManager()  # Инициализация объекта DBManager
    db_manager.create_tables()  # Создание таблиц
    api = HH()
    file_manager = FileManager()

    # Загрузка данных о работодателях и вакансиях
    employers = api.get_employers()
    db_manager.insert_companies(employers)

    vacancies = api.load_vacancies()
    db_manager.insert_vacancies(vacancies)

    while True:
        print("\nВеберите цифру, чтобы получить нужную вам информацию:")
        print("1. Показать компании и количество вакансий")
        print("2. Показать все вакансии")
        print("3. Показать среднюю зарплату по вакансиям")
        print("4. Показать вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("6. Сохранить данные о компаниях в файл")
        print("7. Загрузить данные о компаниях из файла")
        print("8. Выход")

        choice = input("Введите номер действия: ")
        print(f"Вы выбрали: {choice}")

        if choice == "1":
            companies = db_manager.get_companies_and_vacancies_count()
            for company in companies:
                print(f"Компания: {company[0]}, вакансий: {company[1]}")

        elif choice == "2":
            vacancies = db_manager.get_all_vacancies()
            for vacancy in vacancies:
                print(
                    f"Компания: {vacancy[0]}, вакансия: {vacancy[1]}, "
                    f"ЗП: от {vacancy[2]} до {vacancy[3]}, url: {vacancy[4]}"
                )

        elif choice == "3":
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата: {avg_salary}")

        elif choice == "4":
            vacancies = db_manager.get_vacancies_with_higher_salary()
            for vacancy in vacancies:
                print(f"Вакансия: {vacancy[0]}, ЗП: от {vacancy[1]} до {vacancy[2]}, url: {vacancy[3]}")

        elif choice == "5":
            keyword = input("Введите ключевое слово: ")
            vacancies = db_manager.get_vacancies_with_keyword(keyword)
            for vacancy in vacancies:
                print(
                    f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, "
                    f"ЗП: от {vacancy[2]} до {vacancy[3]}, url: {vacancy[4]}"
                )

        elif choice == "6":
            company_ids = input("Введите ID компаний через запятую: ").split(",")
            companies = api.get_companies(company_ids)
            file_manager.save_to_file("companies.json", companies)
            print("Данные о компаниях успешно сохранены в файл.")

        elif choice == "7":
            companies = file_manager.load_from_file("companies.json")
            for company in companies:
                print(f"Компания: {company['name']}, описание: {company["description"]}")

        elif choice == "8":
            print("Выход...")
            db_manager.close()
            break

        else:
            print("Неверный выбор. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
