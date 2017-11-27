a = 5

while a > 0: # Условие истино цикл выполняется 
    print(a)
    a -= 1   # Эта запись равнозначна a = a - 1


# скрипт сам будет запрашивать пароль заново, если он не соответствует требованиям.
# while полезен, так как он возвращает скрипт снова в начало
# проверок, позволяет снова набрать пароль, но при этом не требует перезапуска самого скрипта.
username = input('Введите имя пользователя: ' )
password = input('Введите пароль: ' )
password_correct = False
while not password_correct:
    if len(password) < 8:
        print('Пароль слишком короткий\n')
        password = input('Введите пароль еще раз: ' )
    elif username in password:
        print('Пароль содержит имя пользователя\n')
        password = input('Введите пароль еще раз: ' )
    else:
        print('Пароль для пользователя {} установлен'.format( username ))
        password_correct = True
        
"""
break
"""
# Оператор break позволяет досрочно прервать цикл:
#  - break прерывает текущий цикл и продолжает выполнение следующих выражений
#  - если используется несколько вложенных циклов, break прерывает внутренний
#  - цикл и продолжает выполнять выражения, следующие за блоком
#  - break может использоваться в циклах for и while

for num in range(10):
    if num < 7:
        print(num)
    else:
        break
    
# с циклом while:
i = 0
while i < 10:
    if i == 5:
        break
    else:
        print(i)
    i += 1
 
# скрипт с паролем   
username = input('Введите имя пользователя: ' )
password = input('Введите пароль: ' )
while True:
    if len(password) < 8:
        print('Пароль слишком короткий\n')
    elif username in password:
        print('Пароль содержит имя пользователя\n')
    else:
        print('Пароль для пользователя {} установлен'.format(username))
# завершает цикл while
        break
    password = input('Введите пароль еще раз: ')
    
"""
continue
"""
# Оператор continue возвращает управление в начало цикла. То есть, continue позволяет
# "перепрыгнуть" оставшиеся выражения в цикле и перейти к следующей итерации.
# Пример с циклом for:
for num in range(5):
    if num == 3:
        continue
    else:
        print(num)

# 3 не будет выведено

# Пример с циклом while:

i = 0
while i < 6:
    i += 1
    if i == 3:
       print("Пропускаем 3")
       continue
       print("Это никто не увидит")       # unreachable code - этот кусок кода никогда не выполниться
    else:
       print("Текущее значение")

# Использование continue в примере с запросом пароля

username = input('Введите имя пользователя: ')
password = input('Введите пароль: ')
password_correct = False
while not password_correct:
    if len(password) < 8:
        print('Пароль слишком короткий\n')
    elif username in password:
        print('Пароль содержит имя пользователя\n')
    else:
        print('Пароль для пользователя {} установлен'.format(username))
        password_correct = True
        continue
    password = input('Введите пароль еще раз: ')



"""
pass
"""

# Оператор pass ничего не делает. Фактически, это такая заглушка для объектов.
# Например, pass может помочь в ситуации, когда нужно прописать структуру скрипта.
# Его можно ставить в циклах, функциях, классах. И это не будет влиять на исполнение кода.


for num in range(5):
    if num < 3:
        pass
    else:
        print(num)


# while/else

# блок else выполняется в том случае, если цикл завершил итерацию списка
# но else не выполняется, если в цикле был выполнен break

i = 0

while i < 5:
    print(i)
    i += 1
else:
    print("Конец")

# while с else и break в цикле (из-за break блок else не выполняется):

i = 0
while i < 5:
    if i == 3:
        break
    else:
        print(i)
        i += 1
else:
    print("Конец")

# 0
# 1
# 2


