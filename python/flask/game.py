"""
FLASK 
study part 2

Simple game

- POST /guess   ">", "<", "="
"""
from flask import Flask, request
import random
from flask_wtf import FlaskForm
from wtforms import StringField, validators

app = Flask(__name__)

class CustomValidator(FlaskForm):
    """
    Custom validator Class 
    """
    def choose_from(param): 
        list_of_job = ['IT', 'BANK', 'HR']
        if (param['job']) not in list_of_job:
            print ('Invalid input must be (IT, BANK, HR)')
            return False
        print ('job is valid')
        return True

@app.route('/')
def generate_number():
    global num
    num = random.randint (1,10)  
    return 'number is set'



@app.route('/guess', methods= ['POST'])
def home():
    #num = random.randint (1,10)
    global num
    print(request.form)
    #form = ContactForm(request.form)
    digit = int(request.form ['number'])
    print (digit)
    print ('num ',num)
    if digit > num:
        return '>'
    elif digit < num:
        return '<'
    return '='
 
if __name__ == '__main__':
    #num = random.randint (1,10)   
    app.run(debug=True)
   



















# @app.route('/<user>')
# def username(user):
#     return 'hello, user: ' + user