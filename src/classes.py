import json
from abc import ABC, abstractmethod
import requests


def fetch_vacancies():
    response = requests.get("https://api.hh.ru/vacancies")
    response = response.json()
    return response["items"]


class VacancyHandler(ABC):
    @abstractmethod
    def fetch_vacancies(self):
        pass


class VacancyFetcher(VacancyHandler):

    def fetch_vacancies(self):
        response = requests.get("https://api.hh.ru/vacancies")
        response = response.json()
        return response["items"]


class FileHandler(ABC):

    @abstractmethod
    def save_vacancies_to_file(self):
        pass

    @abstractmethod
    def fetch_data_by_id(self):
        pass

    @abstractmethod
    def clear_file(self):
        pass


class FileOperations(FileHandler):
    @staticmethod
    def save_vacancies_to_file(vacancies):
        with open("../jsons/vacancies.json", "w", encoding="utf-8") as file:
            # Преобразуем данные в строку формата JSON
            json_data = json.dumps(vacancies, ensure_ascii=False, indent=4)
            file.write(json_data)

    # функция которая отчищает весь файл
    def clear_file(self):
        with open("../jsons/vacancies.json", "w"):
            pass

    # функция для нахождения вакансии по id
    def fetch_data_by_id(self, vacancy_id):
        with open("../jsons/vacancies.json", "r") as json_file:
            required_vacancy = None
            data = json.load(json_file)
            for vacancy in data:
                if vacancy["id"] == vacancy_id:
                    required_vacancy = vacancy
            return required_vacancy


class JobVacancy:

    def __init__(self, title, url, salary, requirements):
        self.title = title
        self.url = url
        self.salary = salary
        self.requirements = requirements

    def __gt__(self, other):
        return self.salary > other.salary

# пример работы экземпляров  класса
# vacancy1 = JobVacancy("progger", "dkkdkd", 5000, 400)
# vacancy2 = JobVacancy("progger", "dkkdkd", 6000, 500)
# print(vacancy1.__gt__(vacancy2))
