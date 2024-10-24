import json
from abc import ABC, abstractmethod

import requests


class VacancyHandler(ABC):
    @abstractmethod
    def fetch_vacancies(self, job_title):
        pass

    @abstractmethod
    def sort_jobs(self, job_list, top_count):
        pass

    @abstractmethod
    def search_by_keyword(self, sorted_jobs, keyword):
        pass


class VacancyFetcher(VacancyHandler):

    def fetch_vacancies(self, job_title):
        response = requests.get(f"https://api.hh.ru/vacancies?text={job_title}")
        all_vacancies = response.json()["items"]
        matched_vacancies = []

        for vacancy in all_vacancies:
            if job_title in vacancy["name"]:
                matched_vacancies.append(vacancy)

        return matched_vacancies

    def sort_jobs(self, job_list, top_count):
        def get_salary(vacancy):
            salary_data = vacancy.get("salary")
            if salary_data is None:
                return float('inf')  # Если зарплата отсутствует, ставим очень большое значение
            elif isinstance(salary_data, dict):
                max_salary = salary_data.get("to")
                min_salary = salary_data.get("from")
                if max_salary is None:  # Если верхняя граница равна None
                    return min_salary if min_salary is not None else float('inf')
                return max_salary
            return float('inf')

        sorted_jobs = sorted(job_list, key=get_salary)[:top_count]
        return sorted_jobs

    def search_by_keyword(self, sorted_jobs, keyword):
        results = []
        for vacancy in sorted_jobs:
            if keyword in vacancy["snippet"]["requirement"]:
                results.append(vacancy)

        FileOperations.save_vacancies_to_file(results)
        return results


class FileHandler(ABC):
    @staticmethod
    @abstractmethod
    def save_vacancies_to_file(vacancy_list):
        pass

    @abstractmethod
    def fetch_data_by_id(self, job_id):
        pass

    @abstractmethod
    def clear_file(self):
        pass


class FileOperations(FileHandler):
    @staticmethod
    def save_vacancies_to_file(vacancy_list):
        with open("../jsons/vacancies.json", "w", encoding="utf-8") as file:
            # Преобразуем данные в строку формата JSON
            json_data = json.dumps(vacancy_list, ensure_ascii=False, indent=4)
            file.write(json_data)

    # функция которая очищает весь файл
    def clear_file(self):
        with open("../jsons/vacancies.json", "w"):
            pass

    # функция для нахождения вакансии по id
    def fetch_data_by_id(self, job_id):
        with open("../jsons/vacancies.json", "r") as json_file:
            found_vacancy = None
            data = json.load(json_file)
            for vacancy in data:
                if vacancy["id"] == job_id:
                    found_vacancy = vacancy
            return found_vacancy


class JobVacancy:

    def __init__(self, job_title, job_url, job_salary, job_requirements):
        self.title = job_title
        self.url = job_url
        self.salary = job_salary
        self.requirements = job_requirements

    def __gt__(self, other):
        return self.salary > other.salary
