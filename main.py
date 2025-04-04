from src.hh_api import HHAPI

hh = HHAPI()
print("Получение списка организаций")
result_org_list = hh.get_org()

print("################## DEBUG #####################")
print(f" {len(result_org_list)}")

print("##################### ORG")
for res in result_org_list:
    print(f"{res}")
