Простой принцип работы декоратора

def say1():
	print ('Hello')

scream =say1

# del say1      если удалить say1 то при выводе функции будет ошибка
scream()
say1()         # здесь будет ошибка если раскоментровать del say1 
print ('------------------')

def whisper ():
	def say():
		print ('hello')
		return True
	return say()    # возвращаем 'hello'
	   

whisper()		# возвращаем 'hello'	

print (whisper()) # возвращаем 'hello'  True ( то что возвращает say() )


##########################

def whisper ():
	def say():
		print ('hello')
		return True
	#return say()    # возвращаем 'hello'
	return say    # возвращаем сам объект функцию     

whisper()		# возвращаем 'hello'	


print (whisper())   # <function whisper.<locals>.say at 0x00645108>
print (whisper()()) # возвращаем 'hello'  True ( то что возвращает say() )



################################


print ('%%%%%%%%%%%%%')

def decorator(func):
	def wraper():		# оберка 
		print('code before say2')     
		return func()   # возвращает значение 
	return wraper       # возвращает саму функцию (ссылку на wraper)

@decorator
def say2():
	print ('say2 in funtion say2')


print (say2())  # say2 in funtion say2  None



################################


print ('whith parameters')

def decorator(func):
	def wraper(name):		# оберка 
		print('code before say2')     
		return func(name)   # возвращает значение 
	return wraper       # возвращает саму функцию (ссылку на wraper)

@decorator
def say2(name):
	print (name)


print (say2('anna'))  # say2 in funtion say2  None

"""
whith parameters
code before say2
anna
"""

#---------------------------------------
#Универсальная запись декоратора

print ('whith parameters')

def decorator(func):
	def wraper(*args, **kwargs):		# оберка 
		print('code before say2')     
		return func(*args, **kwargs)   # возвращает значение 
	return wraper       # возвращает саму функцию (ссылку на wraper)

@decorator
def say2(name):
	print (name)


print (say2('anna'))  # say2 in funtion say2  None
=============================================

@A
@B
@C
def f(...):
 ...
равноценна следующей:
def f(...):
 ...
f = A(B(C(f)))
==========================================

   (порядок следования декоратора)
def makebold(fn):
    def wrapped():
        return "<b>" + fn() + "</b>"
    return wrapped
 
def makeitalic(fn):
    def wrapped():
        return "<i>" + fn() + "</i>"
    return wrapped
 
@makebold
@makeitalic

def hello():
    return "hello habr"
 
print (hello()) ## выведет <b><i>hello habr</i></b>



