import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")
redirect_count = len(response.history)
final_redirect = response.history[redirect_count-1].url
print(f"Количество редиректов = {redirect_count}")
print(f"Итоговы URL - {final_redirect}")