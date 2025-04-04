from typing import List

import requests

from config import HH_API_MAX_PER_PAGE, HH_API_MAX_PAGES, HH_API_URL


class HHAPI:

    def __init__(self) -> None:
        self.__url: str = HH_API_URL
        self.__params: dict[str, str] = {"sort_by": "by_vacancies_open", 'page': 0, 'per_page': HH_API_MAX_PER_PAGE }
        self.__name_ids: List[str] = [
            "78638",  # Т-Банк
            "3529",  # СБЕР
            "2324020",  # Точка
            "2173850",  # Аэрофлот Техникс
            "5008932",  # Яндекс Практикум
            "816144",  # ВкусВилл
            "3757",  # Ингосстрах Банк
            "1122462",  # Skyeng
            "2748",  # Ростелеком
            "2180",  # Ozon
        ]
        self.organizations = []

    def get_org_response(self) -> List:
        """
            Подключение к API hh.ru, запрос данных о компаниях
        """

        while self.__params.get('page') != HH_API_MAX_PAGES:
            response = requests.get(self.__url, params=self.__params)
            if response.status_code != 200:
                raise ValueError(f'Ошибка запроса данных: status_code={response.status_code} url={self.__url}')
            else:
                org = response.json()["items"]
                self.organizations.extend(org)
                self.__params['page'] += 1
                print(f"Org page: {self.__params['page']}")
        return self.organizations

    def get_org(self) -> List:
        """
            Получение данных компаний по заданному списку
        """

        name_organization = []
        self.get_org_response()

        # DEBUG
        print(f"Total organizations: {len(self.organizations)}")

        for name_id in self.__name_ids:
            for organization in self.organizations:
                if organization["id"] != name_id:
                    continue
                else:
                    name_organization.append(organization)
        return name_organization
