изменить таблицу dhcp   добавить новое поле
 - таблицу можно поменять из cli sqlite
 
-------------------------------------
Проверка статуса таблицы
.schema dhcp
SELECT * from dhcp;
 
 
                  ALTER TABLE {TableName} ADD COLUMN {NewColumn} {type};
 
ALTER TABLE dhcp ADD COLUMN last_active text;


 
 
 
