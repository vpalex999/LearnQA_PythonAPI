"""
Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_cookie

Этот метод возвращает какую-то cookie с каким-то значением.
Необходимо с помощью функции print() понять что за cookie и с каким значением, и зафиксировать это поведение с помощью assert
"""
import requests


class TestSomeCookies:

    def test_cookie(self):
        api_homework_cookie = "https://playground.learnqa.ru/api/homework_cookie"

        response = requests.get(api_homework_cookie)
        print(response.cookies)
        assert response.cookies["HomeWork"] == "hw_value"
