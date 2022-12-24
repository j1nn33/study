------------------------------------
описание  first
1:
  a - поднять базу postgresql
  b - сделать скрипт мониторинга CPU, RAM, SWAP
  c - скрипт поставить на расписание
  d - таблица в БД (дата и результаты скрипта)
  e - запрос как посмотреть за это время
  f - nginx (страница которая выводит результаты из БД за это время)

2: вопросы по hadoop
   
------------------------------------
общая настройка и проверка инфрастурктуры
# Для быстрого тестирования 
# inventory.ini
# ansible.cfg

Запускать 
~./repo/study/task/first/infra

без ключа
ansible all -i hosts.ini -m ping -k --ask-become-pass

с ключем
ansible.cfg   private_key_file = ~/.ssh/id_rsa

ssh-copy-id username@remote_host

ansible all -i hosts.ini -m ping
ansible all -i hosts.ini -m command -a 'systemctl status chronyd.service'

--------------------------------------
a - поднять базу postgresql

развертывание postgreSQL

ansible-playbook setup_postgreSQL.yml -i hosts.ini

Тестирование инсталяции

su - postgres
psql
получение списка таблиц
\dt *
\q

--------------------------------------
b - сделать скрипт мониторинга CPU, RAM, SWAP

созадем пользователя от которого будет работать скрипт 
useradd tooks
su - tooks

vim test_script
chmod +x monitoring_script.sh
./test_script


--------------------------------------
c - скрипт поставить на расписание            

crontab -e 

* * * * * /home/tooks/monitoring_script.sh


tail -f /var/log/cron

--------------------------------------
d - таблица в БД (дата и результаты скрипта)
  - подготовка базы testdb для пользователя  

sudo -u postgres 
createdb testdb
createuser --superuser tooks

# проверка того что сделали List of databases List of roles

psql 
postgres=# \l
postgres=# \du  

# конфигурим базу
vim /var/lib/pgsql/data/pg_hba.conf
host    all             tooks           127.0.0.1/32            trust

systemctl restart postgresql

# Проверяем результат 
от пользователя tooks
psql -d testdb
# \l

# Созадем базу для скрипта                   

psql -d testdb

CREATE TABLE IF NOT EXISTS monitoring
(
date timestamp,
cpu real,
ram integer,
swap integer
);

\dt
          List of relations
 Schema |    Name    | Type  | Owner
--------+------------+-------+-------
 public | monitoring | table | tooks


Проверяем 

INSERT INTO monitoring (date, cpu, ram, swap) VALUES ('2022-12-24 16:07:02.935', 0.567662, 2896836, 0);
INSERT 0 1

select * from monitoring;
          date           | cpu |   ram   | swap
-------------------------+-----+---------+------
 2022-12-24 16:07:02.935 |   1 | 2896836 |    0


--------------------------------------
e - запрос как посмотреть за это время 
psql -d testdb

SELECT * FROM monitoring WHERE date >= '2022-12-24 18:30:00' AND date< '2022-12-24 18:35:00';
          date           |   cpu    |   ram   | swap
-------------------------+----------+---------+------
 2022-12-24 18:30:02.091 | 0.583652 | 2993788 |    0
 2022-12-24 18:31:01.347 |  0.58372 | 2995656 |    0
 2022-12-24 18:32:01.672 | 0.583806 | 3007700 |    0
 2022-12-24 18:33:01.942 |  0.58388 | 2947140 |    0
 2022-12-24 18:34:02.274 | 0.583959 | 2950736 |    0
(5 rows)

# вывсти послеюднюю запись 
SELECT * FROM monitoring ORDER BY date DESC LIMIT 1;

--------------------------------------
f - nginx (страница которая выводит результаты из БД за это время)  ----------------------

ansible-playbook setup_nginx.yml -i hosts.ini

дорабатываем скрипт

psql -U tooks -d testdb -c 'SELECT * FROM monitoring ORDER BY date DESC LIMIT 1' -o /var/www/html/index.html

--------------------------------------
Разультат

http://192.168.1.236/

date | cpu | ram | swap -------------------------+----------+---------+------ 2022-12-24 21:42:01.361 | 0.609849 | 3163968 | 0 (1 row)