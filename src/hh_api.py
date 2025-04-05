from typing import List

import requests

from config import HH_API_MAX_PER_PAGE, HH_API_MAX_PAGES, HH_API_URL, HH_ORG_LIST


class HHAPI:

    def __init__(self) -> None:
        self.__url: str = HH_API_URL
        self.__params: dict[str, str] = {"sort_by": "by_vacancies_open", 'page': 0, 'per_page': HH_API_MAX_PER_PAGE }
        self.__name_ids: List[str] = HH_ORG_LIST
        self.organizations = []

    def get_org_response(self) -> List:
        """
            Подключение к API hh.ru, запрос данных о компаниях
        """

        while self.__params.get('page') != HH_API_MAX_PAGES:
            response = requests.get(self.__url, params=self.__params)
            if response.status_code != 200:
                # Reached page limit or other request error
                break
            else:
                org = response.json()["items"]
                self.organizations.extend(org)
                self.__params['page'] += 1
                # print(f"Org page: {self.__params['page']}")
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

    @staticmethod
    def get_vac_response(employers: List) -> List:
        """
            Получение вакансий по организациям
        """
        vac = []

        for employer in employers:
            request_params = {'page': 0, "per_page": HH_API_MAX_PER_PAGE}
            while request_params['page'] != HH_API_MAX_PAGES:
                response = requests.get(employer["vacancies_url"], request_params)
                if response.status_code != 200:
                    # Reached page limit or other request error
                    break
                else:
                    vacancies = response.json()["items"]
                    vac.extend(vacancies)
                    request_params['page'] += 1
        return vac

    @staticmethod
    def vac_processing(vacancies_raw: List) -> list[dict[str, int]]:
        """
            Формирование информации о вакансиях для заполнения таблиц в DB
        """
        processed_vac = []
        for vacancy in vacancies_raw:
            if vacancy["salary"] is None:
                salary = 0
            else:
                salary = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
            processed_vac.append(
                {
                    "id": vacancy["id"],
                    "name": vacancy["name"],
                    "salary": salary,
                    "employer": vacancy["employer"]["id"],
                    "url": vacancy["alternate_url"],
                }
            )
        return processed_vac
