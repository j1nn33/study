CREATE DATABASE IF NOT EXISTS test_db location '/data/test_db';
 -- Пересоздание временной таблицы на сонсове CSV Путь с CSV ередается в параметре csv_path
DROP TABLE IF EXISTS test_db.output_csv;
CREATE EXTERNAL TABLE test_db.output_csv(
  1_column string,
  2_column decimal(38,0))
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/data/test_db';

 -- Пересоздаем финальную Parcuet-таблицу  
DROP TABLE IF EXISTS test_db.output_parq;
CREATE TABLE test_db.output_parq (
  1_column string,
  2_column decimal(38,0))
STORED AS PARQUET;

 -- Заполнение финальной таблицы из временной. фильтр Where требуется, чтобы убрать пустые строке, полученные в CSV при выгрузке
INSERT INTO TABLE test_db.output_parq
SELECT 1_column, 2_column FROM test_db.output_csv
WHERE 1_column IS NOT NULL;

 -- Проверям, что данные могут быть прочитанны из финальной таблицы
SELECT * FROM test_db.output_parq LIMIT 3; 
 

 -- Удаляем временну таблицу
#DROP TABLE IF EXISTS test_db.output_csv;

