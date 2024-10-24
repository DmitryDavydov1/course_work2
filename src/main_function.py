from classes import VacancyFetcher


def find_vacancies_by_description():
    # Получаем все вакансии с названием, которое ввел пользователь
    vacancy_fetcher = VacancyFetcher()
    profession_query = input("Введите название профессии: ")
    fetched_vacancies = vacancy_fetcher.fetch_vacancies(profession_query)

    top_vacancy_count = int(input("Введите количество самых высокооплачиваемых вакансий, которые хотите увидеть: "))

    sorted_vacancies = vacancy_fetcher.sort_jobs(fetched_vacancies, top_vacancy_count)

    requirement_keyword = input("Введите ключевое слово: ")

    vacancy_fetcher.search_by_keyword(sorted_vacancies, requirement_keyword)
