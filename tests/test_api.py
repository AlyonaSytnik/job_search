import unittest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from src.api import BaseAPI, HHApi


class TestBaseAPI(unittest.TestCase):
    def test_abstract_method(self):
        """Проверяем, что BaseAPI является абстрактным классом и требует реализации get_vacancies"""
        with self.assertRaises(TypeError):
            BaseAPI()  # Нельзя создать экземпляр абстрактного класса

        class ConcreteAPI(BaseAPI):
            def get_vacancies(self, search_query: str) -> list[dict]:
                return []

        # Конкретная реализация должна работать
        instance = ConcreteAPI()
        self.assertIsInstance(instance, BaseAPI)


class TestHHApi(unittest.TestCase):
    def setUp(self):
        self.api = HHApi()
        self.test_query = "python developer"
        self.mock_response = {
            "items": [
                {"id": "1", "name": "Python Developer", "salary": {"from": 100000}},
                {"id": "2", "name": "Senior Python Developer", "salary": None}
            ]
        }

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тестируем успешный запрос вакансий"""
        # Настраиваем mock
        mock_response = MagicMock()
        mock_response.json.return_value = self.mock_response
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем тестируемый метод
        result = self.api.get_vacancies(self.test_query)

        # Проверяем результаты
        mock_get.assert_called_once_with(
            "https://api.hh.ru/vacancies",
            params={"text": self.test_query, "per_page": 100, "area": 1}
        )
        self.assertEqual(result, self.mock_response["items"])

    @patch('requests.get')
    def test_get_vacancies_http_error(self, mock_get):
        """Тестируем обработку HTTP ошибки"""
        # Настраиваем mock для вызова исключения
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = HTTPError("API error")
        mock_get.return_value = mock_response

        # Проверяем, что исключение пробрасывается
        with self.assertRaises(HTTPError):
            self.api.get_vacancies(self.test_query)

    @patch('requests.get')
    def test_get_vacancies_empty_result(self, mock_get):
        """Тестируем обработку пустого результата"""
        # Настраиваем mock с пустым ответом
        mock_response = MagicMock()
        mock_response.json.return_value = {"items": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Вызываем тестируемый метод
        result = self.api.get_vacancies(self.test_query)

        # Проверяем результаты
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()