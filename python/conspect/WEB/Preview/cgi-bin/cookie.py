#!/usr/bin/python
import os
import http.cookies

# os.environ.get - здесь доступна cookies передаются в виде пар ключ=значение
# для упрощения работы используем http.cookies

cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
name = cookie.get("name")
if name is None:
    print("Set-cookie: name=value")
    print("Content-type: text/html\n")
    print("Cookies!!!")
else:
    print("Content-type: text/html\n")
    print("Cookies:")
    print(name.value)