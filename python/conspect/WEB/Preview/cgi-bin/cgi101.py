#!/usr/bin/python
import cgi

form = cgi.FieldStorage() 			# парсинг данных формы
print('Content-type: text/html\n')	# http-заголовок плюс пустая строка
print('<title>Reply Page</title>') 	# html-разметка ответа
if not 'user' in form:
	print('<h1>Who are you?</h1>')
else:
	print('<h1>Hello <i>%s</i>!</h1>' % cgi.escape(form['user'].value))