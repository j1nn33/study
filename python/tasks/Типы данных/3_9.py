# Найти индекс последнего вхождения элемента.
# Например, для списка num_list, число 10 последний раз встречается с индексом 4; в
# списке word_list, слово 'ruby' последний раз встречается с индексом 6.
# Сделать решение общим (то есть, не привязываться к конкретному элементу в
# конкретном списке) и проверить на двух списках, которые указаны и на разных
# элементах.

num_list = [10, 2, 30, 100, 10, 50, 11, 30, 15, 7]
word_list = ['python', 'ruby', 'perl', 'ruby', 'perl', 'python', 'ruby', 'perl']

number = int(input("ENTER A NUMBER: "))
print("THE NUMBER IS", (number))

rev_list = num_list.copy()  #создаем копию списка
                            # узнаем с каким номером с конца находится необходимый элемет
rev_list.reverse()          # инвертируем список
#print(rev_list)
s = rev_list.index(number)  # под каким номером c в списке идет 1 элемент
c = len(num_list)
#print(c)
print (c-s-1," - last  " )
                            # второй список
word = (input("ENTER A WORD: "))
print("THE WORD IS", (word))

rev_list = word_list.copy() #создаем копию списка
                            # узнаем с каким номером с конца находится необходимый элемет
rev_list.reverse()          # инвертируем список
#print(rev_list)
s = rev_list.index(word)    # под каким номером c в списке идет 1 элемент
c = len(word_list)
#print(c)
print (c-s-1," - last  " )