# Проект по получению данных о компаниях и вакансиях с сайта hh.ru
В рамках проекта можно получить данные об интересующих работодателях и их вакансиях с сайта hh.ru. Информация о них будет сохраняться в таблицах базы данных PostgreSQL.


## Информация о проекте:
Реализован класс `HH` для работы с API hh.ru. В  конструкторе класса прописаны ID компаний с сайта, по которым собирается информация (при желании - их можно заменить на другие).

Реализован класс для взаимодействия с базой данных PostgreSQL - `DBManager`. 
В нем расположены функции: `create_tables` (создает таблицы для компаний и вакансий), `insert_companies` (вставляет данные о компаниях в таблицу), `insert_vacancies` (вставляет данные о вакансиях в таблицу), 
`get_companies_and_vacancies_count` (возвращает список компаний с количеством вакансий у каждой), `get_all_vacancies` (возвращает список всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки на вакансию), `get_avg_salary` (возвращает среднюю зарплату по всем вакансиям), `get_vacancies_with_higher_salary` (возвращает вакансии с зарплатой выше средней), `get_vacancies_with_keyword` (возвращает вакансии, в названии которых содержится ключевое слово).

В классе `FileManager` есть функционал для работы в файлами JSON.

Функция взаимодействия с пользователем реализует интерфейс для работы с данными компаний и вакансий. 
Введя определенную цифру, пользователь сможет получить интересующую его информацию.


## Установка:
Клонируйте репозиторий:
git@github.com:valentinaovsianik/project_BD.git

## Документация:
Подробная документация доступна в комментариях к функциям в коде.

## Лицензия:
На проект распространяется [лицензия MIT](LICENSE).
