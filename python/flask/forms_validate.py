"""
FLASK 
study part 2

1 -  methods=['GET', 'POST'] 
2 POST has a validate data
   - name 
   - email
   - job:
      a) Required field
      b) can choose value in ['IT', 'BANK', 'HR'] 
"""
from flask import Flask, request

from threading import Lock
# pip install flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, validators
#from flask_validator import Validator


class CustomValidator(FlaskForm):
    """
    Custom validator Class 
    can choose value in ['IT', 'BANK', 'HR']
    """
    def choose_from(param): 
        list_of_job = ['IT', 'BANK', 'HR']
        if (param['job']) not in list_of_job:
            print ('Invalid input must be (IT, BANK, HR)')
            return False
        print ('job is valid')
        return True
  
   
class ContactForm(FlaskForm):
    name = StringField(label='Name', validators=[
        validators.Length(min=4, max=25)
    ])
    email = StringField(label='E-mail', validators=[
        validators.Length(min=6, max=35),
        validators.Email()
    ])
    # valid for standart
    job = StringField(label='JOB', validators=[
        validators.Length(min=1, max=6),
        #validators.Optional(),           # Not required parametr job
        validators.DataRequired(),
    ])
    

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY='This key must be secret!',
    WTF_CSRF_ENABLED=False,
)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        form = ContactForm(request.form)
        print(form.validate())

        if form.validate() and CustomValidator.choose_from(request.form):     # вызов кастомного валидатора
            return ('valid', 200)
        else:
            return ('invalid', 400)


    if request.method == 'GET':
        return 'hello world!', 200


if __name__ == '__main__':
    app.run()
