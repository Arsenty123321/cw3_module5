import psycopg2
from typing import List
from config import get_config_db

class DBSettings:
    """
        Загружает конфиг для работы с БД
    """
    def __init__(self) -> None:
        self.__database_name: str = "coursework3"
        self.__params: dict[str, str] = get_config_db()

    @property
    def database_name(self) -> str:
        return self.__database_name

    @property
    def params(self) -> dict[str, str]:
        return self.__params


class DBSetup(DBSettings):

    def __init__(self) -> None:
        super().__init__()

    def init_db(self) -> None:
        """
            Удаляет старую и создает новую БД
        """

        conn = psycopg2.connect(dbname="postgres", **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        cur.close()
        conn.close()

    def init_db_tables(self) -> None:
        """
            Создает таблицы в БД
        """

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE organization (
                    organization_id INTEGER PRIMARY KEY,
                    organization_name VARCHAR,
                    organization_url TEXT,
                    open_vacancies INTEGER
                )
            """
            )

            cur.execute(
                """
                CREATE TABLE vacancies (
                    vacancy_name VARCHAR, 
                    vacancies_id INT NOT NULL,
                    vacancies_url TEXT,
                    salary INTEGER,
                    organization_id INT REFERENCES organization(organization_id)
                )
            """
            )

        conn.commit()
        conn.close()

    def fill_db_tables(self, organizations: List, vacancies: List) -> None:
        """
            Заполняет таблицы БД
        """

        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            for org in organizations:
                cur.execute(
                    """
                    INSERT INTO organization (organization_id, organization_name, organization_url, open_vacancies)
                    VALUES (%s, %s, %s, %s)
                    RETURNING organization_id
                    """,
                    (org["id"], org["name"], org["url"], org["open_vacancies"]),
                )

                for vac in vacancies:
                    if vac["employer"] == org["id"]:
                        cur.execute(
                            """
                            INSERT INTO vacancies (organization_id, vacancy_name, vacancies_id, vacancies_url, salary)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (vac["employer"], vac["name"], vac["id"], vac["url"], vac["salary"]),
                        )
        conn.commit()
        conn.close()
