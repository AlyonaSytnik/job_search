class Vacancy:
    def __init__(self, title: str, url: str, salary: dict, description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary: dict) -> dict:
        if not salary:
            return {"from": 0, "to": 0, "currency": "не указана"}
        return {
            "from": salary.get("from", 0),
            "to": salary.get("to", 0),
            "currency": salary.get("currency", "не указана"),
        }

    @property
    def avg_salary(self) -> float:
        if self.salary["from"] and self.salary["to"]:
            return (self.salary["from"] + self.salary["to"]) / 2
        return self.salary["from"] or self.salary["to"] or 0

    def __lt__(self, other) -> bool:
        return self.avg_salary < other.avg_salary

    def __gt__(self, other) -> bool:
        return self.avg_salary > other.avg_salary

    def __eq__(self, other) -> bool:
        return self.avg_salary == other.avg_salary

    def __str__(self) -> str:
        salary_from = f"от {self.salary['from']}" if self.salary["from"] else ""
        salary_to = f"до {self.salary['to']}" if self.salary["to"] else ""
        currency = (
            self.salary["currency"] if self.salary["currency"] != "не указана" else ""
        )

        salary_parts = [salary_from, salary_to, currency]
        salary = " ".join(part for part in salary_parts if part).strip()
        salary = salary if salary else "не указана"

        return (
            f"Вакансия: {self.title}\n"
            f"Зарплата: {salary}\n"
            f"Ссылка: {self.url}\n"
            f"Описание: {self.description[:200]}...\n"
            "----------------------------------------"
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_json: list[dict]) -> list["Vacancy"]:
        return [
            cls(
                title=v.get("name", "Без названия"),
                url=v.get("alternate_url", "#"),
                salary=v.get("salary"),
                description=(
                    v.get("snippet", {}).get("requirement", "")
                    or v.get("snippet", {}).get("responsibility", "")
                    or ""
                ),
            )
            for v in vacancies_json
        ]
