import pytest
from unittest.mock import patch, mock_open
from src.utils import (
    print_vacancies,
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    save_filtered_results,
    Vacancy
)


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy(
            title="Python Developer",
            description="Разработчик на Python с опытом работы",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            url="http://example.com"
        ),
        Vacancy(
            title="Java Developer",
            description="Разработчик Java с знанием Spring",
            salary={"from": 120000, "to": 180000, "currency": "RUR"},
            url="http://example.com"
        ),
        Vacancy(
            title="Senior Python Developer",
            description="Опытный Python разработчик",
            salary={"from": 150000, "to": 200000, "currency": "RUR"},
            url="http://example.com"
        )
    ]


class TestPrintVacancies:
    @patch("builtins.print")
    def test_print_empty_list(self, mock_print):
        print_vacancies([])
        mock_print.assert_called_once_with("Вакансий не найдено.")

    @patch("builtins.print")
    def test_print_vacancies(self, mock_print, sample_vacancies):
        print_vacancies(sample_vacancies[:2])
        assert mock_print.call_count == 2


class TestFilterVacancies:
    def test_filter_without_words(self, sample_vacancies):
        result = filter_vacancies(sample_vacancies, [])
        assert result == sample_vacancies

    def test_filter_with_one_word(self, sample_vacancies):
        result = filter_vacancies(sample_vacancies, ["python"])
        assert len(result) == 2
        assert all("Python" in v.title for v in result)

    def test_filter_with_multiple_words(self, sample_vacancies):
        result = filter_vacancies(sample_vacancies, ["разработчик", "опыт"])
        assert len(result) == 2  # Только 2 вакансии содержат оба слова
        titles = {v.title for v in result}
        assert "Python Developer" in titles
        assert "Senior Python Developer" in titles

    def test_filter_case_insensitive(self, sample_vacancies):
        result = filter_vacancies(sample_vacancies, ["JAVA"])
        assert len(result) == 1
        assert result[0].title == "Java Developer"