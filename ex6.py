"""
Ex6: Длинный редирект
Необходимо написать скрипт, который создает GET-запрос на метод: https://playground.learnqa.ru/api/long_redirect
С помощью конструкции response.history необходимо узнать, сколько редиректов происходит от изначальной точки назначения до итоговой. И какой URL итоговый.
Ответ опубликуйте в виде ссылки на коммит со скриптом, а также укажите количество редиректов и конечный URL.
"""
import requests


response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)

print(f"Counts of redirects: {len(response.history)}")
print(f"The last URL is: {response.url}")
