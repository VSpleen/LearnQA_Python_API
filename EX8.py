import requests
import time


response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
rep_json1 = response1.json()

response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":rep_json1["token"]})
rep_json2 = response2.json()

if rep_json2["status"]=="Job is NOT ready":
    print(f"Задача еще не готова, получен ответ{response2.text}, требуется подожать {rep_json1['seconds']} секунд")
    time.sleep(rep_json1["seconds"])


response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token":rep_json1["token"]})
rep_json3 = response3.json()
if rep_json3["status"] == "Job is ready" or True:
    try:
        print(f"Результат = {rep_json3['result']}")
    except KeyError:
        print("Резуьтат отсутствует")
