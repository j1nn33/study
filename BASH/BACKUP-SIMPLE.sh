#!/bin/bash
echo "=========================="
# переменные базы данных
DBUSER="root"             # Имя пользователя базы данных
DBPASS=""                 # Пароль пользователя базы данных
DBNAME="newdatabase"      # Имя базы данных
DBARC=$DBNAME.sql         # Имя архива базы данных
PREFIX=`date +%F--%H-%M`  # Дополнение даты 2018-12-20--21-31

# переменные файлов
SCR_DIR="/var/www"        # Корневая директория файлов
ARCHIVE="arhive.tar"      # Имя архива файлов 
DEST_DIR="/vrem/"

#-----MAIN-------
echo ""
echo "Архивируем базу данных со сжатием"

# mysqldump -u [username] -p [password] [database] > [dump_name.sql]


mysqldump --user=$DBUSER --password=$DBPASS --databases $DBNAME  > $DBNAME.sql.back$PREFIX

echo ""
echo "===========Архивируем файлы======="
#Создаем файловый архив со сжатием

tar -czvf $DEST_DIR$ARCHIVE.gz $SCR_DIR

