""""
ДЛЯ СИСТЕМНОГО АДМИНИСТРАТРОВАНИЯ
"""""
"------------РАБОТА С ФАЙЛАМИ"
"""
'r' – открыть файл для чтения;
'w' – открыть файл для записи;
'x' – открыть файл с целью создания, если файл существует,
      то вызов функции open завершится с ошибкой;
'a' – открыть файл для записи, при этом новые 
      данные будут добавлены в конец файла, без удаления существующих;
'b' – бинарный режим;
't' – текстовый режим;
'+' – открывает файл для обновления

file.closed – возвращает true если файл закрыт 
              и false в противном случае;
file.mode   – возвращает режим доступа к файлу, 
              при этом файл должен быть открыт;
"""
    "ОТКРЫТИЕ И ЗАКРЫТИЕ ФАЙЛОВ"
f = open("test.txt", "r")
print("file.closed: " + str(f.closed))
"file.closed: False"
print("file.mode: " + f.mode)
"file.mode: r"
print("file.name: " + f.name)
"file.name: test.txt"

    "ЧТЕНИЕ ДАННЫХ ИЗ ФАЙЛА"

"read(размер) считывает из файла определенное количество символов"

f = open("test.txt", "r")
f.read()
"1 2 3 4 5 \n Work with file \n"
f.close()

f = open("test.txt", "r")
f.read(5)
"1 2 3"
f.close()

"Метод readline() позволяет считать строку из открытого файла."
f = open("test.txt", "r")
f.readline()
"1 2 3 4 5 \n""
f.close()

"Построчное считывание с помощью оператора for"
f = open("test.txt", "r")
for line in f:
    print (line)

"1 2 3 4 5"
"Work with file"
f.close()

    "ЗАПИСЬ ДАННЫХ В ФАЙЛ"

f = open("test.txt", "a")
f.write("Test string")
"11"
f.close()

"tell() возвращает текущую позицию “условного курсора” в файле."
f = open("test.txt", "r")
f.read(5)
'1 2 3'
f.tell()
"5"
f.close()

"Метод seek(позиция) выставляет позицию в файле."
"1 2 3 4 5"
f = open("test.txt", "r")
f.tell()
"0"
f.seek(8)
"8"
f.read(1)
"5"
f.tell()
"9"
f.close()

"""with при его использовании нет необходимости закрывать файл, 
при завершении работы с ним, эта операция будет выполнена автоматически."""

with open ("test.txt", "r") as f:
    for line in f:
    print(line)


"""1 2 3 4 5

Work with file
Test string"""
f.closed
True



