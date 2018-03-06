                SQL -  категории:
 DDL (Data Definition Language)      - язык описания данных
 DML (Data Manipulation Language)    - язык манипулирования данными
 DCL (Data Control Language)         - язык определения доступа к данным
 TCL (Transaction Control Language)  - язык управления транзакциями

                    операторы (перечислены не все операторы):
        DDL
        
 CREATE - создание новой таблицы, СУБД, схемы
 ALTER - изменение существующей таблицы, колонки
 DROP - удаление существующих объектов из СУБД
        
        DML
        
 SELECT - выбор данных
 INSERT - добавление новых данных
 UPDATE - обновление существующих данных
 DELETE - удаление данных
        
        DCL
        
 GRANT - предоставление пользователям разрешения на чтение/запись определенных объектов в СУБД
 REVOKE - отзыв ранее предоставленных разрешений
       
        TCL
        
 COMMIT Transaction - применение транзакции
 ROLLBACK Transaction - откат всех изменений, сделанных в текущей транзакции
 
######################################################################## 
       
       SQLite
 Метакоманды  - относятся к SQLite ; - не ставиться (к SQL не имеет никакого отношения)
       
 создать БД (или открыть уже созданную)

sqlite3 nameDB.db
sqlite3 .help
sqlite3 .exit


########################################################################
       
       SQL
       
"""create - позволяет создавать таблицы"""
 
qlite> CREATE table switch (            # создаем таблицу switch
...> mac text not NULL primary key,
...> hostname text,
...> model text,
...> location text
...> );

sqlite> create table switch (mac text not NULL primary key, hostname text, model text, location text);


# мы описали таблицу switch: определили, какие поля будут в таблице, и значения какого типа будут в них находиться

поле - mac является первичным ключом (так как MAC-адрес должен быть уникальным.)
     - поле должно быть уникальным
     - в нем не может находиться значение NULL (в SQLite это надо задавать явно)

qlite> .database   # просмотреть базы 


# На данный момент записей в таблице нет, есть только ее определение. Просмотреть определение можно такой командой

sqlite> .schema switch
CREATE TABLE switch (
mac text not NULL primary key,
hostname text,
model text,
location text
);

"""DROP - Оператор DROP удаляет таблицу вместе со схемой и всеми данными."""
 
# Удалить таблицу можно так:
sqlite> DROP table switch;

""" insert используется для добавления данных в таблицу."""

# Есть несколько вариантов добавления записей, в зависимости от того, все ли поля
# будут заполнены, и будут ли они идти по порядку определения полей или нет.

1 - Если указываются значения для всех полей, добавить запись можно таким образом
    (порядок полей должен соблюдаться):
        
sqlite> INSERT into switch values ('0010.A1AA.C1CC', 'sw1', 'Cisco 3750', 'London, Green Str');

2 - Если нужно указать не все поля или указать их в произвольном порядке, используется такая запись:
    
sqlite> INSERT into switch (mac, model, location, hostname)
   ...> values ('0020.A2AA.C2CC', 'Cisco 3850', 'London, Green Str', 'sw2');
   
""" select позволяет запрашивать информацию в таблице"""

sqlite> SELECT * from switch;
0010.A1AA.C1CC|sw1|Cisco 3750|London, Green Str
0020.A2AA.C2CC|sw2|Cisco 3850|London, Green Str
       
# select * означает, что нужно вывести все поля таблицы. Следом указывается, из какой таблицы запрашиваются данные: from switch .

sqlite> .headers ON                 # включеине отображение полей 

sqlite> SELECT * from switch;
mac|hostname|model|location
0010.A1AA.C1CC|sw1|Cisco 3750|London, Green Str
0020.A2AA.C2CC|sw2|Cisco 3850|London, Green Str

sqlite> .mode column                 # включает отображение в виде колонок:
sqlite> SELECT * from switch;
mac            hostname    model     location
-------------- ---------- ---------- -----------------
0010.A1AA.C1CC sw1        Cisco 3750 London, Green Str
0020.A2AA.C2CC sw2        Cisco 3850 London, Green Str

"""
Если нужно сделать так, чтобы эти параметры использовались по умолчанию,
добавьте их в файл .sqliterc в домашнем каталоге пользователя, под которым вы работаете
"""

#  содержимое файла  /home/user/.sqliterc 
.headers on
.mode column

""" WHERE используется для уточнения запроса"""
sqlite> SELECT * from switch WHERE model = 'Cisco 3850';

mac            hostname   model      location
-------------- ---------- ---------- -----------------
0020.A2AA.C2CC sw2        Cisco 3850 London, Green Str
0040.A4AA.C2CC sw4        Cisco 3850 London, Green Str
0050.A5AA.C3CC sw5        Cisco 3850 London, Green Str

Оператор WHERE позволяет указывать не только конкретное значение поля. 
Если добавить к нему оператор LIKE, можно указывать шаблон поля.
LIKE с помощью символов _ и % указывает, на что должно быть похоже значение:
    _ - обозначает один символ или число
    % - обозначает ноль, один или много символов
    
sqlite> SELECT * from switch WHERE model LIKE '%3750';

mac            hostname   model      location
-------------- ---------- ---------- -----------------
0010.A1AA.C1CC sw1        Cisco 3750 London, Green Str
0030.A3AA.C1CC sw3        Cisco 3750 London, Green Str
0060.A6AA.C4CC sw6        C3750      London, Green Str

""" ALTER позволяет менять существующую таблицу: добавлять новые колонки или переименовывать таблицу"""
# добавление полей
# mngmt_ip - IP-адрес коммутатора в менеджмент VLAN
# mngmt_vid - VLAN ID (номер VLAN) для менеджмент VLAN
 
ALTER table switch ADD COLUMN mngmt_ip text;
ALTER table switch ADD COLUMN mngmt_vid integer;

""" UPDATE используется для изменения существующей записи таблицы"""

# обычно  UPDATE используется вместе с оператором WHERE, чтобы уточнить, какую именно запись необходимо изменить.
UPDATE switch set mngmt_ip = '10.255.1.1' WHERE hostname = 'sw1';
UPDATE switch set mngmt_vid = 255 WHERE hostname = 'sw1';

UPDATE switch set mngmt_ip = '10.255.1.2', mngmt_vid = 255 WHERE hostname = 'sw2';


""" REPLACE используется для добавления или замены данных в таблице."""

# Когда возникает нарушение условия уникальности поля, выражение с оператором REPLACE:
# удаляет существующую строку, которая вызвала нарушение добавляет новую строку

# У выражения REPLACE есть два вида:
# ниже происходит запиена записи
sqlite> INSERT OR REPLACE INTO switch
...> VALUES ('0030.A3AA.C1CC', 'sw3', 'Cisco 3850', 'London, Green Str', '10.255.1.3', 255);

sqlite> REPLACE INTO switch
...> VALUES ('0030.A3AA.C1CC', 'sw3', 'Cisco 3850', 'London, Green Str', '10.255.1.3', 255);

# При добавлении записи, для которой не возникает нарушения уникальности поля, replace работает как обычный inser
REPLACE INTO switch
...> VALUES ('0080.A8AA.C8CC', 'sw8', 'Cisco 3850', 'London, Green Str', '10.255.1.8', 255);


""" delete используется для удаления записей."""

DELETE from switch where hostname = 'sw8';

""" ORDER BY используется для сортировки вывода по определенному полю,
по возрастанию или убыванию. Для этого он добавляется к оператору SELECT. """

SELECT * from switch ORDER BY hostname ASC;   # по возрастанию 

SELECT * from switch ORDER BY mngmt_ip DESC;  # по убыванию

""" AND позволяет группировать несколько условий:"""

select * from switch where model = 'Cisco 3750' and ip LIKE '10.0.%';
select * from switch where model LIKE '%3750%' and ip LIKE '10.0.%';

""" OR """

select * from switch where model = 'Cisco 3750' or model = 'Cisco 3850';

""" IN """

select * from switch where model in ('Cisco 3750', 'C3750');

""" NOT """
select * from switch where model not in ('Cisco 3750', 'C3750');





