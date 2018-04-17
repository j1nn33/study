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

  # (порядок следования декоратора)
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