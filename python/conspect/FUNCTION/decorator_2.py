# Декораторы — обычные функции, которые принимают в качестве аргумента
# другую функцию.

def decorator(func):
    def decorated(*args, **kwargs):
        print('before')
        result = func(*args, **kwargs)
        print('after')
        return result
    return decorated

def s(a,b):
    print(a+b)

s = decorator(s)
s(1, 2)

# более удобный способ обернуть функцию
@decorator
def m(a,b):
    print (a*b)

m(2,3)

# декоратор времени выполнения программы
import time
def timer(func):
    def decorated(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print ("Время выполнения функции: %f" % (time.time()-t))
        return result
    return decorated

@timer
def func(x, y):
    return x + y

func(1,2)


# Функцию можно обернуть в несколько декораторов. В этом случае они 
# «выполняются» сверху вниз.
def pause(f):
    def decorated(*args, **kwargs):
        time.sleep(1)
        return f(*args, **kwargs)

    return decorated

@decorator
@timer
@pause
def func(x, y):
    return x + y

func(1,2)


# В декоратор можно передавать параметры:
def pause(t):
    def wrapper(f):
        def tmp(*args, **kwargs):
            time.sleep(t)
            return f(*args, **kwargs)
        return tmp

    return wrapper

@pause(2)
def func(x, y):
    return x + y

print (func(1, 2))


# существуют два втроенных декоратора для методов классов
class Spam:
    num_instances = 0

    @classmethod
    def count(cls):
        cls.num_instances += 1

    @staticmethod
    def print_count():
        print(Spam.num_instances)

    def __init__(self):
        self.count()

a, b, c = Spam(), Spam(), Spam()
print(a.num_instances)



