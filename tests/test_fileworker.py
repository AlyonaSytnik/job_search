import json
import os
from unittest.mock import mock_open, patch

import pytest

from src.fileworker import BaseWorker, JSONWorker, Vacancy


class TestBaseWorker:
    def test_abstract_methods(self):
        """Проверяем, что BaseWorker является абстрактным классом"""
        with pytest.raises(TypeError):
            BaseWorker()  # Нельзя создать экземпляр абстрактного класса

        class ConcreteWorker(BaseWorker):
            def add_vacancy(self, vacancy: Vacancy) -> None:
                pass

            def get_vacancies(self, criteria: dict = None) -> list[Vacancy]:
                return []

            def delete_vacancy(self, vacancy: Vacancy) -> None:
                pass

        # Конкретная реализация должна работать
        instance = ConcreteWorker()
        assert isinstance(instance, BaseWorker)


class TestJSONWorker:
    TEST_FILENAME = "test_vacancies.json"
    SAMPLE_VACANCIES = [
        {
            "title": "Python Developer",
            "description": "Разработчик Python",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "url": "http://example.com",
        },
        {
            "title": "Java Developer",
            "description": "Разработчик Java",
            "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            "url": "http://example.com",
        },
    ]

    @pytest.fixture
    def worker(self):
        """Фикстура для создания экземпляра JSONWorker с тестовым файлом"""
        worker = JSONWorker(self.TEST_FILENAME)
        yield worker
        # Удаляем тестовый файл после каждого теста
        if os.path.exists(self.TEST_FILENAME):
            os.remove(self.TEST_FILENAME)

    @pytest.fixture
    def sample_vacancy(self):
        """Фикстура для создания тестовой вакансии"""
        return Vacancy(
            title="Python Developer",
            description="Разработчик Python",
            salary={"from": 100000, "to": 150000, "currency": "RUR"},
            url="http://example.com",
        )

    def test_add_vacancy(self, worker, sample_vacancy):
        """Тестируем добавление вакансии"""
        worker.add_vacancy(sample_vacancy)

        with open(worker.filename, "r") as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]["title"] == sample_vacancy.title

    def test_get_vacancies_no_criteria(self, worker, sample_vacancy):
        """Тестируем получение всех вакансий без критериев"""
        worker.add_vacancy(sample_vacancy)
        vacancies = worker.get_vacancies()

        assert len(vacancies) == 1
        assert vacancies[0].title == sample_vacancy.title

    def test_get_vacancies_with_salary_criteria(self, worker):
        """Тестируем фильтрацию по зарплате"""
        for vacancy_data in self.SAMPLE_VACANCIES:
            worker.add_vacancy(Vacancy(**vacancy_data))

        # 1. Вакансии, полностью попадающие в диапазон
        criteria = {"salary": {"from": 100000, "to": 200000}}  # Обе вакансии
        assert len(worker.get_vacancies(criteria)) == 2

        # 2. Только Python Developer (100-150k)
        criteria = {"salary": {"from": 100000, "to": 150000}}
        filtered = worker.get_vacancies(criteria)
        assert len(filtered) == 1
        assert filtered[0].title == "Python Developer"

        # 3. Только Java Developer (120-180k)
        criteria = {"salary": {"from": 120000, "to": 180000}}
        filtered = worker.get_vacancies(criteria)
        assert len(filtered) == 1
        assert filtered[0].title == "Java Developer"

        # 4. Узкий диапазон - нет подходящих
        criteria = {"salary": {"from": 90000, "to": 95000}}
        assert len(worker.get_vacancies(criteria)) == 0

    def test_get_vacancies_with_keyword_criteria(self, worker):
        """Тестируем фильтрацию по ключевому слову"""
        for vacancy_data in self.SAMPLE_VACANCIES:
            worker.add_vacancy(Vacancy(**vacancy_data))

        criteria = {"keyword": "java"}
        filtered = worker.get_vacancies(criteria)

        assert len(filtered) == 1
        assert filtered[0].title == "Java Developer"

    def test_delete_vacancy(self, worker, sample_vacancy):
        """Тестируем удаление вакансии"""
        worker.add_vacancy(sample_vacancy)
        worker.delete_vacancy(sample_vacancy)

        vacancies = worker.get_vacancies()
        assert len(vacancies) == 0

    def test_load_vacancies_file_not_found(self, worker):
        """Тестируем загрузку из несуществующего файла"""
        assert worker._load_vacancies() == []

    def test_load_vacancies_invalid_json(self, worker):
        """Тестируем обработку невалидного JSON"""
        with open(worker.filename, "w") as f:
            f.write("invalid json")

        assert worker._load_vacancies() == []

    @patch(
        "builtins.open", new_callable=mock_open, read_data=json.dumps(SAMPLE_VACANCIES)
    )
    def test_load_vacancies_success(self, mock_file, worker):
        """Тестируем успешную загрузку вакансий"""
        result = worker._load_vacancies()
        assert len(result) == 2
        assert result[0]["title"] == "Python Developer"

    @patch("builtins.open", side_effect=PermissionError("No write permission"))
    def test_save_vacancies_error(self, mock_file, worker):
        """Тестируем обработку ошибки при сохранении"""
        with pytest.raises(PermissionError):
            worker._save_vacancies(self.SAMPLE_VACANCIES)
