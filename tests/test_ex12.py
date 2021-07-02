"""
Необходимо написать тест, который делает запрос на метод: https://playground.learnqa.ru/api/homework_header


Этот метод возвращает headers с каким-то значением.
Необходимо с помощью функции print() понять что за headers
и с каким значением, и зафиксировать это поведение с помощью assert
"""
import requests


class TestSomeCookies:

    def test_cookie(self):
        api = "https://playground.learnqa.ru/api/homework_header"

        response = requests.get(api)
        print(response.headers)
        assert response.headers["x-secret-homework-header"] == "Some secret value"
