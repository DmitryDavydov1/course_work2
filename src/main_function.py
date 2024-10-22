import requests
from classes import FileOperations


def find_vacancies_by_description():
    # Получаем все вакансии с названием, которое ввел пользователь

    search_query = input("Введите название профессии: ")
    response = requests.get(f"https://api.hh.ru/vacancies?text={search_query}")
    vacancies = response.json()["items"]
    filtered_vacancies = []
    top_vacancy_list = []

    for vacancy in vacancies:
        if search_query in vacancy["name"]:
            filtered_vacancies.append(vacancy)

    top_vacancy_count = int(input("Введите количество самых высокооплачиваемых вакансий, которые хотите увидеть: "))

    def extract_salary(vacancy):
        salary_info = vacancy.get("salary")
        if salary_info is None:
            return float('inf')  # Если зарплата отсутствует, ставим очень большое значение
        elif isinstance(salary_info, dict):
            upper_bound = salary_info.get("to")
            lower_bound = salary_info.get("from")
            if upper_bound is None:  # Если верхняя граница равна None
                return lower_bound if lower_bound is not None else float('inf')
            return upper_bound
        return float('inf')

    sorted_vacancies = sorted(filtered_vacancies, key=extract_salary)[:top_vacancy_count]

    requirement_keyword = input("Введите ключевое слово: ")
    for vacancy in sorted_vacancies:
        if requirement_keyword in vacancy["snippet"]["requirement"]:
            top_vacancy_list.append(vacancy)

    FileOperations.save_vacancies_to_file(top_vacancy_list)
    return top_vacancy_list
