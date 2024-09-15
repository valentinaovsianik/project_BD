import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import DictCursor

from config import config


class DBManager:
    """Класс для взаимодействия с базой данных PostgreSQL."""

    def __init__(self):
        """Инициализирует подключение к базе данных."""
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cursor = self.conn.cursor(cursor_factory=DictCursor)
            print("Подключение к базе данных успешно")
        except OperationalError as e:
            print(f"Ошибка при подключении к базе данных: {e}")

    def create_tables(self):
        """Создает таблицы для компаний и вакансий."""
        create_table_queries = """
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255),
            description TEXT,
            industry VARCHAR(255)
        );

        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            company_id INT REFERENCES companies(company_id),
            name VARCHAR(255) NOT NULL,
            salary_from INT,
            salary_to INT,
            currency VARCHAR(10),
            published_at TIMESTAMP,
            url VARCHAR(255)
        );
        """
        self.cursor.execute(create_table_queries)
        self.conn.commit()

    def insert_companies(self, companies):
        """Вставляет данные о компаниях в таблицу."""
        insert_query = """
        INSERT INTO companies (company_id, name, url, description, industry)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (company_id) DO NOTHING;
        """
        for company in companies:
            self.cursor.execute(
                insert_query,
                (
                    company.get("id"),
                    company.get("name"),
                    company.get("url"),
                    company.get("description"),
                    company.get("industry"),
                ),
            )
        self.conn.commit()

    def insert_vacancies(self, vacancies):
        """Вставляет данные о вакансиях в таблицу."""
        insert_query = """
        INSERT INTO vacancies (vacancy_id, company_id, name, salary_from, salary_to, currency, published_at, url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (vacancy_id) DO NOTHING;
        """
        for vacancy in vacancies:
            self.cursor.execute(
                insert_query,
                (
                    vacancy.get("id"),
                    vacancy.get("employer", {}).get("id"),
                    vacancy.get("name"),
                    vacancy.get("salary", {}).get("from"),
                    vacancy.get("salary", {}).get("to"),
                    vacancy.get("salary", {}).get("currency"),
                    vacancy.get("published_at"),
                    vacancy.get("url"),
                ),
            )
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Возвращает список компаний с количеством вакансий у каждой."""
        query = """
        SELECT c.name, COUNT(v.vacancy_id) AS vacancies_count
        FROM companies c
        LEFT JOIN vacancies v ON c.company_id = v.company_id
        GROUP BY c.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Возвращает список всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки на вакансию."""
        query = """
        SELECT c.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.company_id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Возвращает среднюю зарплату по всем вакансиям."""
        query = """
        SELECT AVG((salary_from + salary_to)/2) AS avg_salary
        FROM vacancies
        WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL;
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Возвращает вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        query = """
        SELECT name, salary_from, salary_to, url
        FROM vacancies
        WHERE (salary_from + salary_to)/2 > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Возвращает вакансии, в названии которых содержится ключевое слово."""
        query = """
        SELECT c.name AS company_name, v.name AS vacancy_name, v.salary_from, v.salary_to, v.url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.company_id
        WHERE v.name ILIKE %s;
        """
        self.cursor.execute(query, (f"%{keyword}%",))
        return self.cursor.fetchall()

    def close(self):
        """Закрывает соединение с базой данных."""
        self.cursor.close()
        self.conn.close()
