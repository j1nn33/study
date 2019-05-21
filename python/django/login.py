https://wsvincent.com/django-user-authentication-tutorial-login-and-logout/

#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

создать в корне проекта такую структуру

(<nameProject>) $ mkdir templates
(<nameProject>) $ mkdir templates/registration
(<nameProject>) $ touch templates/registration/login.html


# <nameProject><nameProject>/settings.py
TEMPLATES = [
    {
        ...
        'DIRS': ['./templates',],
        ...
    },
]


LOGIN_REDIRECT_URL = '/'

http://127.0.0.1:8000/accounts/login/

Create a homepage

(<nameProject>)  $ touch templates/base.html
(<nameProject>)  $ touch templates/home.html


Сделать редирект в urls

<nameProject><nameProject>/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView # new

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), # new
]


(при тестировании важно включать ссылки из терминила или новые для актульного отображения)

-----------------------------------------------


Для подключения аутентификации на весь сайт добаляем в базовый шаблон html
wrapper.html  пример object


{% if user.is_authenticated %}
  {% block content %}

  {% endblock %}
 {% else %}

 <p align="center"><strong>Вам необходимо войти на сайт</strong></p>
 <p align="center"><a class="btn btn-info"href="{% url 'login' %}">login</a></p>


 {% endif %}

=========================

{% block content %}

{% if form.errors %}
<p>Your username and password didnt match. Please try again.</p>
{% endif %}

{% if next %}
    {% if user.is_authenticated %}
    <p>Your account doesnt have access to this page. To proceed,
    please login with an account that has access.</p>
    {% else %}
    <p>Please login to see this page.</p>
    {% endif %}
{% endif %}

<form method="post" action="{% url 'login' %}">
{% csrf_token %}
<table>
<tr>
    <td>{{ form.username.label_tag }}</td>
    <td>{{ form.username }}</td>
</tr>
<tr>
    <td>{{ form.password.label_tag }}</td>
    <td>{{ form.password }}</td>
</tr>
</table>

<input type="submit" value="login">
<input type="hidden" name="next" value="{{ next }}">
</form>

{# Assumes you setup the password_reset view in your URLconf #}
<p><a>Lost password?</a></p>

{% endblock %}


===================================================================


def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
        else:
            # Return a 'disabled account' error message
            ...
    else:
        # Return an 'invalid login' error message.
        ...

-----------------------------------------------

def logout_view(request):
    logout(request)
    # Redirect to a success page.

---------------------------------------------



from django.conf import settings
from django.shortcuts import redirect

def my_view(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
... или отображение сообщения об ошибке:

from django.shortcuts import render

def my_view(request):
    if not request.user.is_authenticated():
        return render(request, 'myapp/login_error.html')
    # ...
Декоратор logi



========================