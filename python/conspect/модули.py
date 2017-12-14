модуль - любой файл с расширением .py
import - выполняет загрузку другого файла и обеспечивает доступ к его содержимому
содержимое становиться доступным внешнему миру через его атрибуты
""" ПРИМЕР
# cat myfile.py       -  содержимое файла myfile.py
title = "The Meaning of Life"
"""
- доступ к атрибуту title
1 способ
import myfile               # получение доступа к атрибутам модуля
print (myfile.title)        # object.attribute
# The Meaning of Life

2 способ  

from myfile import title    # получение копии имени из модуля 
print (title)
# The Meaning of Life
