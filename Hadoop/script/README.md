#### Курс Data Engineer
##### 1 hadoop
##### 2 Pandas
##### 3 Spark
##### 4 визуализация данных
##### 5 Feature Engineering
##### 6 HQL
##### 7 ETL


##### 1 hadoop  task1 
Скрипт выгрузки данных из таблицы 

bash - скрипт 

1 - отдельный файл с запросом (селекты и условия) в отдельном файле *.hql  (export.hql)
2 - результат работы скрипта в формате *.csv
3 - путь к таблице hadoop храниться отдельно 


script/task_1
export.hql      - скрипт запроса к базе данных
data_export.sh  - скрипт который читает данные запросом export.hql и загружает их в в формате parquet скриптом upload.hql
upload.hql      - скрипт по загрузке parquet

##### 2 Pandas 
##### 3 Spark 
##### 4 визуализация данных 
##### 5 Feature Engineering
##### 6 HQL
##### 7 ETL