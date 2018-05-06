# Работа с исключениями try/except/else/finally

#       try/except

====================================================================================
except name:                        = Перехватывает только указанное исключение.
except name as value:               = Перехватывает указанное исключение и 
                                      получает соответствующий экземпляр.
except (name1, name2):              = Перехватывает любое из перечисленных исключений.
except (name1, name2) as value:     = Перехватывает любое из перечисленных 
                                      исключений и получает соответствующий экземпляр.
else:                               = Выполняется, если не было исключений.
finally:                            = Этот блок выполняется всегда
======================================================================================
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

-------------DEBUG----------

# raise Exception ('это сообщение об ошибке.') # raise  генерит исключение

def boxPrint (symbol, width, height):
    if len(symbol) !=1:
        raise Exception ('Переменная символ должна быть односимвольной')
    if width <=2:
        raise Exception ('Width должно быть больше 2')
    if height <=2:
        raise Exception ('heighh должно быть больше 2')    
    print ('sybol', symbol)
    
try:
    #boxPrint('q',3, 4)    # sybol q
    #boxPrint('qq',3,3)    # возникло исключение Переменная символ должна быть односимвольной
    #boxPrint('q',1,3)     #возникло исключение Width должно быть больше 2
    boxPrint('q',3,1)     #возникло исключение heighh должно быть больше 2
except Exception as err:
    print ('возникло исключение '+str(err))
    
-------------------------------------
запись отладочной информации в файл
---------------------------------

import traceback
try:
    raise Exeption('Это сообщение об ошибке')
except:
    errorFile = open('errorInfo.txt','w')
    errorFile.write(traceback.format_exc())
    errorFile.close()
    print('information about error in errorInfo.txt')
    
--------------------------------------------
протоколирование 
--------------------------------------------
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')
# запись сообщений в файл
# logging.basicConfig(filename="sample.log", level=logging.INFO)
def factorial(n):
    logging.debug('Start of factorial(%s%%)' % (n))
    total = 1
    for i in range(1, n + 1):
        total *= i
        logging.debug('i is ' + str(i) + ', total is ' + str(total))
    return total
    logging.debug('End of factorial(%s%%)' % (n))

print(factorial(5))
logging.debug('End of program')
        
"""

2018-02-19 19:07:28,062 - DEBUG - Start of program
2018-02-19 19:07:28,062 - DEBUG - Start of factorial(5%)
2018-02-19 19:07:28,062 - DEBUG - i is 1, total is 1
2018-02-19 19:07:28,062 - DEBUG - i is 2, total is 2
2018-02-19 19:07:28,062 - DEBUG - i is 3, total is 6
2018-02-19 19:07:28,062 - DEBUG - i is 4, total is 24
2018-02-19 19:07:28,062 - DEBUG - i is 5, total is 120
120
2018-02-19 19:07:28,062 - DEBUG - End of program
"""














