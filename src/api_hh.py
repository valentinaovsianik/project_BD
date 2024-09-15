import requests


class HH:
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        """Конструктор класса."""
        self.__url = "https://api.hh.ru/"
        self._headers = {"User-Agent": "HH-User-Agent"}
        self._params = {"per_page": 100, "page": 0, "only_with_salary": True}
        self.employers = [9694561, 903500, 1912942, 3246641, 5667343, 9301808, 6031, 10571093, 10581539, 4475, 205656]

    def get_employers(self):
        """Загрузка работодателей с API."""
        employers_info = []
        for employer_id in self.employers:
            try:
                temp_url = f"{self.__url}employers/{employer_id}"
                response = requests.get(temp_url)
                if response.status_code == 200:
                    employer_data = response.json()
                    employers_info.append(employer_data)
                else:
                    print(f"Ошибка при получении данных о работодателе {employer_id}: {response.status_code}")
            except Exception as e:
                print(f"Ошибка: {e}")
        return employers_info

    def load_vacancies(self):
        """Загрузка вакансий с API с учетом пагинации."""
        vacancy_info = []
        for employer_id in self.employers:
            self._params["employer_id"] = employer_id
            page = 0
            while True:
                self._params["page"] = page
                vacancy_url = f"{self.__url}vacancies"
                try:
                    response = requests.get(vacancy_url, headers=self._headers, params=self._params)
                    if response.status_code == 200:
                        vacancies = response.json().get("items", [])
                        if not vacancies:
                            break  # Если на текущей странице нет вакансий, выходим из цикла
                        vacancy_info.extend(vacancies)
                        page += 1
                    else:
                        print(f"Ошибка при получении вакансий для работодателя {employer_id}: {response.status_code}")
                        break
                except Exception as e:
                    print(f"Ошибка: {e}")
                    break
        return vacancy_info

    def get_companies(self, company_ids):
        """Метод для получения данных о компаниях по их ID."""
        companies_info = []
        for company_id in company_ids:
            try:
                url = f"{self.__url}employers/{company_id}"
                response = requests.get(url, headers=self._headers)
                if response.status_code == 200:
                    company_data = response.json()
                    companies_info.append(company_data)
                else:
                    print(f"Ошибка при получении данных о компании {company_id}: {response.status_code}")
            except Exception as e:
                print(f"Ошибка: {e}")
        return companies_info
