
IndentationError: expected an indented block
"проблема в отступах"
TypeError: Can't convert 'int' object to str implicitly
"операции над строкой и числом (сложение или вычитани и т д)"

NameError: name ‘a’ is not de1ned
"преременная а не существует"

IndentationError: expected an indented block.
"нужен отступ"
TabError: inconsistent use of tabs and spaces in indentation
"проверить табулвяцию"

UnboundLocalError: local variable ‘a’ referenced before assignment.
"попытка обращения к локаольной переменной которая еще не была создана"


print ( "start" )
try :
    val = int ( input ( "input number: " ))
    tmp = 10 / val
    print (tmp)
except ValueError :
    print ( "ValueError!" )
except ZeroDivisionError :
    print ( "ZeroDivisionError!" )
except :
    print ( "Error!" )
print ( "stop" )
finally :
    print ( "Finally code" )


print ( "start" )
try :
    val = int ( input ( "input number: " ))
    tmp = 10 / val
    print (tmp)
except Exception as e:
    print ( "Error! " + str (e))
print ( "stop" )
finally :
    print ( "Finally code" )


print ( "start" )
try :
    val = int ( input ( "input number: " ))
    tmp = 10 / val
    print (tmp)
except ValueError as ve:
    print ( "ValueError! {0}" .format(ve))
except ZeroDivisionError as zde:
    print ( "ZeroDivisionError! {0}" .format(zde))
except Exception as ex:
    print ( "Error! {0}" .format(ex))
print ( "stop" )
finally :
    print ( "Finally code" )

"""Если необходимо выполнить какой-то программный код,
в случае если в процессе выполнения блока try не возникло
исключений, то можно использовать оператор else."""
try :
    f = open ( "tmp.txt" , "r" )
for line in f:
    print (line)
    f.close()
except Exception as e:
    print (e)
else :
    print ( "File was readed" )


"""Для принудительной генерации исключения используется инструкция raise .
Таким образом, можно “вручную” вызывать исключения при необходимости."""
try :
    raise Exception ( "Some exception" )
except Exception as e:
    print ( "Exception exception " + str (e))
