import pytest
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy(
            title="Python Developer",
            url="http://example.com/python",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            description="Разработчик на Python с опытом работы"
        ),
        Vacancy(
            title="Java Developer",
            url="http://example.com/java",
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            description="Разработчик Java с знанием Spring"
        ),
        Vacancy(
            title="Intern",
            url="http://example.com/intern",
            salary={},
            description="Стажировка для начинающих разработчиков"
        )
    ]


class TestVacancyInit:
    def test_init_with_full_salary(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={"from": 1000, "to": 2000, "currency": "USD"},
            description="Test description"
        )
        assert vacancy.title == "Test"
        assert vacancy.salary["from"] == 1000
        assert vacancy.salary["to"] == 2000
        assert vacancy.salary["currency"] == "USD"

    def test_init_with_empty_salary(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary=None,
            description="Test description"
        )
        assert vacancy.salary["from"] == 0
        assert vacancy.salary["to"] == 0
        assert vacancy.salary["currency"] == "не указана"

    def test_init_with_partial_salary(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={"from": 1000, "currency": "EUR"},
            description="Test description"
        )
        assert vacancy.salary["from"] == 1000
        assert vacancy.salary["to"] == 0
        assert vacancy.salary["currency"] == "EUR"


class TestVacancyProperties:
    def test_avg_salary_both_values(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={"from": 1000, "to": 2000, "currency": "USD"},
            description="Test description"
        )
        assert vacancy.avg_salary == 1500

    def test_avg_salary_only_from(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={"from": 1000, "currency": "USD"},
            description="Test description"
        )
        assert vacancy.avg_salary == 1000

    def test_avg_salary_only_to(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={"to": 2000, "currency": "USD"},
            description="Test description"
        )
        assert vacancy.avg_salary == 2000

    def test_avg_salary_no_values(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={},
            description="Test description"
        )
        assert vacancy.avg_salary == 0


class TestVacancyComparisons:
    def test_less_than(self, sample_vacancies):
        assert sample_vacancies[0] < sample_vacancies[1]  # 125k < 150k

    def test_greater_than(self, sample_vacancies):
        assert sample_vacancies[1] > sample_vacancies[0]  # 150k > 125k

    def test_equal(self):
        v1 = Vacancy(
            title="A",
            url="http://a.com",
            salary={"from": 1000, "to": 2000},
            description="Test"
        )
        v2 = Vacancy(
            title="B",
            url="http://b.com",
            salary={"from": 1500},
            description="Test"
        )
        assert v1 == v2  # Обе имеют avg_salary = 1500


class TestVacancyStringRepresentation:
    def test_str_with_full_salary(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={"from": 1000, "to": 2000, "currency": "USD"},
            description="Test description"
        )
        s = str(vacancy)
        assert "Вакансия: Test" in s
        assert "Зарплата: от 1000 до 2000 USD" in s
        assert "Ссылка: http://test.com" in s
        assert "Описание: Test description" in s

    def test_str_with_partial_salary(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={"to": 2000, "currency": "USD"},
            description="Test description"
        )
        s = str(vacancy)
        assert "Зарплата: до 2000 USD" in s

    def test_str_with_no_salary(self):
        vacancy = Vacancy(
            title="Test",
            url="http://test.com",
            salary={},
            description="Test description"
        )
        s = str(vacancy)
        # Обновляем проверку в соответствии с фактической реализацией
        assert "Зарплата: не указана" in s
        assert "Вакансия: Test" in s
        assert "Ссылка: http://test.com" in s
        assert "Описание: Test description" in s


class TestVacancyClassMethods:
    def test_cast_to_object_list(self):
        json_data = [
            {
                "name": "Developer",
                "alternate_url": "http://dev.com",
                "salary": {"from": 1000, "to": 2000, "currency": "USD"},
                "snippet": {
                    "requirement": "Python knowledge",
                    "responsibility": "Develop apps"
                }
            },
            {
                "name": "Manager",
                "alternate_url": "http://manager.com",
                "salary": None,
                "snippet": {}
            }
        ]
        vacancies = Vacancy.cast_to_object_list(json_data)
        assert len(vacancies) == 2
        assert vacancies[0].title == "Developer"
        assert vacancies[0].salary["from"] == 1000
        assert vacancies[1].title == "Manager"
        assert vacancies[1].salary["from"] == 0
        assert "Python knowledge" in vacancies[0].description