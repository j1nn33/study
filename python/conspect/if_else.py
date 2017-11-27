                         #if/elif/else
"""
Nолько if является обязательным, elif и else опциональны:
         Проверка if всегда идет первой.
         После оператора if должно быть какое-то условие: если это условие выполняется
                                                          (возвращает True), то действия в блоке if выполняются.
      elif делает несколько разветвлений блоков elif может быть много
      else выполняется в том случае, если ни одно из условий if или elif не было истинным.
"""

a = 9
if a == 10:
    print('a равно 10')
elif a < 10:
    print('a меньше 10')
else:
    print('a больше 10')
        
# a меньше 10

# Оператор in позволяет выполнять проверку на наличие элемента в 
# последовательности (например, элемента в списке или подстроки в строке):
'Fast' in 'FastEthernet'
# True

# При использовании со словарями условие in выполняет проверку по ключам словаря:
r1 = {
    'IOS': '15.4',
    'IP': '10.255.0.1',
    'hostname': 'london_r1',
    'location': '21 New Globe Walk',
    'model': '4451',
    'vendor': 'Cisco'}
'IOS' in r1
# True
'4451' in r1
# False

# Операторы and, or, not

# В Python оператор and возвращает не булево значение, а значение одного из операторов.
# Если оба операнда являются истиной, результатом выражения будет последнее значение:
 true
'string1' and 'string2'
# 'string2'
'string1' and 'string2' and 'string3'
# 'string3'
# Если один из операторов является ложью, результатом выражения будет первое ложное значение:
 false
'' and 'string1'
# ''
'' and [] and 'string1'
#''

# Оператор or
# При оценке операндов возвращается первый истинный операнд:
'' or 'string1'
# 'string1'
'' or [] or 'string1'
# 'string1'
'string1' or 'string2'
# 'string1'

# Если все значения являются ложью, возвращается последнее значение:
'' or [] or {}
# {}
# Важная особенность работы оператора or - операнды, которые находятся после
# истинного, не вычисляются:
'' or sorted([44,1,67])
# [1, 44, 67]
'' or 'string1' or sorted([44,1,67])
# 'string1'

 (Ternary expressions)
 
s = [1, 2, 3, 4]
result = True if len(s) > 5 else False


# игра угадай число
import random
number = random.randint(0, 101)

while True:

    answer = input("Введите число : ")
    if not answer or answer == "exit":
        break

    if not answer.isdigit():
        print("input right digit")
        continue

    user_answer = int(answer)

    if user_answer > number:
        print("digit <")
    elif user_answer < number:
        print("digit >")
    else:
        print("you win")
        break
