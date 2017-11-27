# Работа с исключениями try/except/else/finally

#       try/except

# Когда в программе возникает исключение, она сразу завершает работу.
# Для работы с исключениями используется конструкция try/except :

try:
    2/0
except ZeroDivisionError:
    print("You can't divide by zero")

# You can't divide by zero


# - сначала выполняются выражения, которые записаны в блоке try
# - если при выполнения блока try не возникло никаких исключений, блок except
#   пропускается, и выполняется дальнейший код
# - если во время выполнения блока try в каком-то месте возникло исключение,
#   оставшаяся часть блока try пропускается
#     -  если в блоке except указано исключение, которое возникло, выполняется код в
#        блоке except
#     -  если исключение, которое возникло, не указано в блоке except, выполнение
#        программы прерывается и выдается ошибка

#  строка 'Cool!' в блоке try не выводится:

try:
    print("Let's divide some numbers")
    2/0
    print('Cool!')
except ZeroDivisionError:
    print("You can't divide by zero")

# Let's divide some numbers
# You can't divide by zero

# В конструкции try/except может быть много except, если нужны разные действия в
# зависимости от типа ошибки.
try:
    a = input("Введите первое число: ")
    b = input("Введите второе число: ")
    print("Результат: ", int(a)/int(b))
except ValueError:
    print("Пожалуйста, вводите только числа")
except ZeroDivisionError:
    print("На ноль делить нельзя")
# или

try:
    a = input("Введите первое число: ")
    b = input("Введите второе число: ")
    print("Результат: ", int(a)/int(b))
except (ValueError, ZeroDivisionError):
    print("Что-то пошло не так...")

# try/except/else

# В конструкции try/except есть опциональный блок else. Он выполняется в том случае,
# если не было исключения

try:
    a = input("Введите первое число: ")
    b = input("Введите второе число: ")
    result = int(a)/int(b)
except (ValueError, ZeroDivisionError):
    print("Что-то пошло не так...")
else:
    print("Результат в квадрате: ", result**2)

# try/except/finally

# Блок finally -Он выполняется всегда, независимо от того, 
# было ли исключение или нет. Сюда ставятся действия, 
#которые надо выполнить в любом случае. 
#Например, это может быть закрытие файла.

try:
    a = input("Введите первое число: ")
    b = input("Введите второе число: ")
    result = int(a)/int(b)
except (ValueError, ZeroDivisionError):
    print("Что-то пошло не так...")
else:
    print("Результат в квадрате: ", result**2)
finally:
    print("Вот и сказочке конец, а кто слушал - молодец.")

####### Использование исключения

while True:
    a = input("Введите число: ")
    b = input("Введите второе число: ")
try:
    result = int(a)/int(b)
except ValueError:
    print("Поддерживаются только числа")
except ZeroDivisionError:
    print("На ноль делить нельзя")
else:
    print(result)
break

# Тот же код только без исключений

while True:
    a = input("Введите число: ")
    b = input("Введите второе число: ")
    if a.isdigit() and b.isdigit():
        if int(b) == 0:
            print("На ноль делить нельзя")
         else:
             print(int(a)/int(b))
             break
     else:
         print("Поддерживаются только числа")
         

"""Для принудительной генерации исключения используется инструкция raise .
Таким образом, можно “вручную” вызывать исключения при необходимости."""
try :
    raise Exception ( "Some exception" )
except Exception as e:
    print ( "Exception exception " + str (e))
