from abc import ABC, abstractmethod

import requests


class BaseAPI(ABC):
    @abstractmethod
    def get_vacancies(self, search_query: str) -> list[dict]:
        pass


class HHApi(BaseAPI):
    def get_vacancies(self, search_query: str) -> list[dict]:
        url = "https://api.hh.ru/vacancies"
        params = {"text": search_query, "per_page": 100, "area": 1}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()["items"]
