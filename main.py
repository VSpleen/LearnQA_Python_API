import requests

methods = ["GET", "POST", "PUT", "DELETE"]



for every in methods:
    response = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={"method":every})
    print(f"Ответ для запроса get c method = {every} - {response.text}")
    response = requests.post("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":every})
    print(f"Ответ для запроса post c method = {every} - {response.text}")
    response = requests.put("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":every})
    print(f"Ответ для запроса put c method = {every} - {response.text}")
    response = requests.delete("https://playground.learnqa.ru/ajax/api/compare_query_type", data={"method":every})
    print(f"Ответ для запроса delete c method = {every} - {response.text}")
    print("\n\n")
