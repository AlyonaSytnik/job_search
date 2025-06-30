import json
from abc import ABC, abstractmethod

from .vacancy import Vacancy


class BaseWorker(ABC):
    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, criteria: dict = None) -> list[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


class JSONWorker(BaseWorker):
    def __init__(self, filename: str = "vacancies.json"):
        self.filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self._load_vacancies()
        vacancies.append(vacancy.__dict__)
        self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: dict = None) -> list[Vacancy]:
        vacancies_data = self._load_vacancies()
        vacancies = [Vacancy(**v) for v in vacancies_data]

        if not criteria:
            return vacancies

        filtered = []
        for v in vacancies:
            match = True
            for key, value in criteria.items():
                if key == "salary":
                    # Проверяем что зарплата указана
                    if not v.salary:
                        match = False
                    else:
                        # Вакансия должна полностью попадать в запрошенный диапазон
                        salary_from = v.salary.get('from', 0)
                        salary_to = v.salary.get('to', float('inf'))
                        if not (value['from'] <= salary_from and salary_to <= value['to']):
                            match = False
                elif key == "keyword":
                    if value.lower() not in (v.title + v.description).lower():
                        match = False
                elif getattr(v, key, None) != value:
                    match = False
            if match:
                filtered.append(v)
        return filtered

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self._load_vacancies()
        vacancies = [v for v in vacancies if v != vacancy.__dict__]
        self._save_vacancies(vacancies)

    def _load_vacancies(self) -> list[dict]:
        try:
            with open(self.filename, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_vacancies(self, vacancies: list[dict]) -> None:
        with open(self.filename, "w") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)
