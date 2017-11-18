name = input("Введи свое имя: ")
f"Привет, {name}!"
#Введи свое имя:
  Александр

#'Привет, Александр!'
# Базовые типы: численные типы

# Целые числа (int)
num = 13
num = -10
num = 100_000_000
print(num)
print(type(num)) # покзывает тип num
# Вещественные числа (float)
num = 100_000.000_001
# Конвертация типов:
num = 150.2
print(type(num))

#<class 'float'>

num = int(num)
print(num, type(num))
num = float(num)
print(num, type(num))

#150 <class 'int'>
#150.0 <class 'float'>
#----------
#Меняем местами значения 2-х переменных:

a = 100
b = 200
print(a, b)
a, b = b, a
print(a, b)
#100 200
#200 100
#------------

bool(12)
#True
bool(0)

#False

x = 12
y = False
print(x or y)
#12

x = 12
z = "boom"
print(x and z)
#boom
#------- СТРОКИ------
example_string = "Курс про Python на Coursera"
print(example_string)
example_string = 'Курс про "Python" на "Coursera"' = "Курс про \"Python\" на \"Coursera\""
# "Cырые" (r-строки):
example_string = "Файл на диске c:\\\\"
print(example_string)
example_string = r"Файл на диске c:\\"
print(example_string)
#Файл на диске c:\\
#Файл на диске c:\\
#
#Срезы строк [start:stop:step]

example_string = "Москва"
example_string[::-1]

#'авксоМ'

#Форматирование строк

template = "%s — главное достоинство программиста. (%s)"
template % ("Лень", "Larry Wall")

#'Лень — главное достоинство программиста. (Larry Wall)'

"{} не лгут, но {} пользуются формулами. ({})".format(
    "Цифры", "лжецы", "Robert A. Heinlein"
)

#'Цифры не лгут, но лжецы пользуются формулами. (Robert A. Heinlein)'


"{num} Кб должно хватить для любых задач. ({author})".format(
    num=640, author="Bill Gates"
)

#'640 Кб должно хватить для любых задач. (Bill Gates)'

subject = "оптимизация"
author = "Donald Knuth"

f"Преждевременная {subject} — корень всех зол. ({author})"

#'Преждевременная оптимизация — корень всех зол. (Donald Knuth)'

 Модификаторы форматирования:

num = 8
f"Binary: {num:#b}"

#'Binary: 0b1000'

num = 2 / 3
print(num)

print(f"{num:.3f}")
#0.6666666666666666
#0.667
#кодирование и декодирование строки
example_string = "привет"
encoded_string = example_string.encode(encoding="utf-8")
print(encoded_string)
print(type(encoded_string))
#b'\xd0\xbf\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82'
#class 'bytes'>
decoded_string = encoded_string.decode()
print(decoded_string)
#привет