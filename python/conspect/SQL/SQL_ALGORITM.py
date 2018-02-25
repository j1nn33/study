sqlite3 .help
sqlite3 .exit
ctrl+z  - exit
.database      # инфа по базам полдключенным к  одному сервису
.schema switch # инфа по таблице
--------------------
1) 
mydatabase.db3 .dump > res.sql    # bakup mydatabase в скрипт res.sql
res.db3 < res.sql                 # восстановление из скрипта res.sql в базу res.db3 
2)
.output my.sql        # данные будут выводиться в файл my.sql
.dump                 # делаем дамп данных
.output stdout        # возвращаем вывод данных на экран
3)
.backup backup.txt    # если несколько баз данных подключено то бекапиться будет база main 
-------------------
  # импорт данных в базу данных 
.import file_name.csv table_name


.read file.txt                   # заполнение таблици из файла
.save testsavedb.sample          # сохранение таблици в  файл
------
#  содержимое файла  /home/user/.sqliterc 
.headers on
.mode column


------

1. создание базы данных 

# создать БД (или открыть уже созданную)
sqlite3 nameDB.db              
# создание таблицы switch (схемы)
sqlite> create table switch (mac text not NULL primary key, hostname, textmodel text,
location text); 
# Удалить таблицу можно так:
sqlite> DROP table switch;

"""
sqlite3 switch
.schema switch
SELECT * from switch;

"""

2. работа с таблицей 


sqlite> INSERT into switch values ('0010.A1AA.C1CC', 'sw1', 'Cisco 3750', 'London, Green Str');
sqlite> SELECT * from switch;
