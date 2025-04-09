import psycopg2
from typing import Any
from src.db_setup import DBSettings


class DBManager(DBSettings):

    def __init__(self) -> None:
        super().__init__()

    def execute_query(self, query: str) -> Any:
        """
            Подключается к БД
        """
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_companies_and_vacancies_count() -> str:
        """
            Получает список всех компаний и количество вакансий у каждой компании
        """
        query = """
            SELECT organization.organization_name, COUNT(vacancies.vacancy_name) FROM organization, vacancies
            WHERE organization.organization_id=vacancies.organization_id
            GROUP BY organization.organization_name
            """
        return query

    @staticmethod
    def get_all_vacancies() -> str:
        """
            Получает список всех вакансий с указанием названия компании,
            названия вакансии и зарплаты и ссылки на вакансию
        """

        query = """
            SELECT organization_name, vacancy_name, salary, vacancies_url FROM organization
            INNER JOIN vacancies ON organization.organization_id=vacancies.organization_id
            """
        return query

    @staticmethod
    def get_avg_salary() -> str:
        """
            Получает среднюю зарплату по вакансиям
        """

        query = """
            SELECT AVG(salary) FROM vacancies
            """
        return query

    @staticmethod
    def get_vacancies_with_higher_salary() -> str:
        """
            Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям
        """

        query = """
            SELECT vacancy_name, salary, vacancies_url FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies)
            """
        return query

    @staticmethod
    def get_vacancies_with_keyword(user_query: str) -> str:
        """
            Получает список всех вакансий, в названии которых содержатся переданные в метод слова
        """

        query = f"""
            SELECT vacancy_name, salary, vacancies_url, organization_name FROM vacancies
            INNER JOIN organization ON vacancies.organization_id=organization.organization_id
            WHERE LOWER(vacancy_name) LIKE '%{user_query.lower()}%'
            """
        return query
