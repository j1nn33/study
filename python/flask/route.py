"""
FLASK 
study part 1

1 - get user     --> retun user
2 - get 2 digit  --> return summa
3 - get 3 string --> return maxlen str
3 - get file relative path form folder --> reutrn 'YES' if exist   
"""
from flask import Flask
import os

app = Flask(__name__)

"""
@app.route('/')
def index():
    return 'hello world!'
"""
@app.route('/<string:user>')
def task_one(user):
    return 'hello world! '+user

""" 
# task_two ver 1
  
@app.route('/<one>/<two>/')
def task_two(one, two):
    tree = int(one) + int(two)
    return 'summa = ' + str(tree)
"""
# task_two ver 2

@app.route('/<int:one>/<int:two>/')
def task_two(one, two):
    tree = one + two
    return 'summa = ' + str(tree)

@app.route('/<str1>/<str2>/<str3>/')
def task_tree(str1, str2, str3):
    str_max = max (str1, str2, str3)
    return 'max string is  = ' + str_max


@app.route('/<file_name>/')
def task_four(file_name):
    path = os.path.abspath (file_name)
    if os.path.isfile(file_name):
        ansver = 'YES'
    else:
        ansver = 'NO'
   
    return 'max string is  = ' + ansver + 'path ' + path


if __name__ == '__main__':
    
    app.run(debug=True)



















# @app.route('/<user>')
# def username(user):
#     return 'hello, user: ' + user