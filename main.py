from src.db_setup import DBSetup
from src.dbmanager import DBManager
from src.hh_api import HHAPI
from typing import List

# Запросы в HH API
hh = HHAPI()
print("Получение списка организаций")
result_org_list = hh.get_org()
print("Получение списка всех вакансий")
result_vac_raw = hh.get_vac_response(result_org_list)
print(f"Количество вакансий: {len(result_vac_raw)}")
result_vac = hh.vac_processing(result_vac_raw)

# Инициализация БД
dbsetup = DBSetup()
print("Подготовка/заполнение БД")
# Удаляем/Cоздаем БД
dbsetup.init_db()
# Создаем таблицы
dbsetup.init_db_tables()
# Наполняем таблицы
dbsetup.fill_db_tables(result_org_list, result_vac)

dbmanager = DBManager()

def print_results(results: List):
    """
        Построчная распечатка результатов
    """
    for res in results:
        print(f"{res}")

def main() -> None:

    print(
        """
        
        Выберите запрос необходимой информации из базы данных:
        1 - список всех компаний и количество вакансий у каждой компании
        2 - список всех вакансий с указанием компании, вакансии, зарплаты и ссылки на вакансию
        3 - средняя зарплата по вакансиям
        4 - список всех вакансий, у которых зарплата выше средней
        5 - поиск вакансий по ключевому слову 
        """
    )

    user_input = input()

    if user_input == "1":
        results = dbmanager.execute_query(dbmanager.get_companies_and_vacancies_count())
        print_results(results)

    elif user_input == "2":
        results = dbmanager.execute_query(dbmanager.get_all_vacancies())
        print_results(results)

    elif user_input == "3":
        results = dbmanager.execute_query(dbmanager.get_avg_salary())
        print(results)

    elif user_input == "4":
        results = dbmanager.execute_query(dbmanager.get_vacancies_with_higher_salary())
        print_results(results)

    elif user_input == "5":
        print(f"\nВведите ключевое слово для поиска вакансии: ")
        user_request = input()
        results = dbmanager.execute_query(dbmanager.get_vacancies_with_keyword(user_request))
        print_results(results)

    else:
        print(f"\n\nНеверный запрос, повторите попытку")

if __name__ == "__main__":
    main()
