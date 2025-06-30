import json

from .vacancy import Vacancy


def print_vacancies(vacancies: list[Vacancy]) -> None:
    if not vacancies:
        print("Вакансий не найдено.")
        return

    for ind, vacancy in enumerate(vacancies, 1):
        print(f"{ind}. {vacancy}")


def filter_vacancies(
    vacancies: list[Vacancy], filter_words: list[str]
) -> list[Vacancy]:
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        text = (vacancy.title + vacancy.description).lower()
        if all(word.lower() in text for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(
    vacancies: list[Vacancy], salary_range: str
) -> list[Vacancy]:
    if not salary_range:
        return vacancies

    try:
        salary_from, salary_to = map(int, salary_range.split("-"))
        return [v for v in vacancies if salary_from <= v.avg_salary <= salary_to]
    except ValueError:
        print("Некорректный формат. Используйте формат: FROM-TO")
        return vacancies


def sort_vacancies(vacancies: list[Vacancy]) -> list[Vacancy]:
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: list[Vacancy], top_n: int) -> list[Vacancy]:
    return vacancies[:top_n]


def save_filtered_results(vacancies: list[Vacancy]):
    if not vacancies:
        return
    vacancies_data = [vacancy.__dict__ for vacancy in vacancies]

    with open("vacancies.json", "w", encoding="utf-8") as f:
        json.dump(vacancies_data, f, ensure_ascii=False, indent=2)
