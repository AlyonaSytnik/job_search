from src.api import HHApi
from src.fileworker import JSONWorker
from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, print_vacancies,
                       save_filtered_results, sort_vacancies)
from src.vacancy import Vacancy


def user_interaction():
    hh_api = HHApi()
    json_worker = JSONWorker(filename="vacancies.json")

    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input("Введите диапазон зарплат (например: 100000-150000): ")
    hh_vacancies = hh_api.get_vacancies(search_query)
    vacancies_list = Vacancy.cast_to_object_list(hh_vacancies)

    for vacancy in vacancies_list:
        json_worker.add_vacancy(vacancy)

    all_vacancies = json_worker.get_vacancies()
    filtered_vacancies = filter_vacancies(all_vacancies, filter_words)
    ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)
    sorted_vacancies = sort_vacancies(ranged_vacancies)
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
    save_filtered_results(top_vacancies)
    print(f"\nНайдено {len(top_vacancies)} вакансий:")
    print_vacancies(top_vacancies)


if __name__ == "__main__":
    user_interaction()
