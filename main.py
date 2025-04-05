from src.db_setup import DBSetup
from src.hh_api import HHAPI

hh = HHAPI()
print("Получение списка организаций")
result_org_list = hh.get_org()

print("################## DEBUG #####################")
print(f" {len(result_org_list)}")

print("##################### ORG")
for res in result_org_list:
    print(f"{res}")

print("##################### VAC")
print("Получение списка вакансий")
result_vac_raw = hh.get_vac_response(result_org_list)
print(f"Количество вакансий: {len(result_vac_raw)}")

print("Получение списка вакансий")
result_vac = hh.vac_processing(result_vac_raw)


dbsetup = DBSetup()
print("# Удаляем/Cоздаем БД")
dbsetup.init_db()
print("# Создаем таблицы")
dbsetup.init_db_tables()
print("# Наполняем таблицы")
dbsetup.fill_db_tables(result_org_list, result_vac)

