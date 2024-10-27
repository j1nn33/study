### Чек лист тестирования кластера
#### HDFS 
#### HIVE
#### BEELINE
#### IMPALA
#### SPARK-SHELL
#### HBASE

###### HDFS
```
# отображение файловой структуры 
# отсутвие missing block
# аналих нод клатсера (кто отвалился)
hdfs dfs -ls /
hdfs fsck -list-corruptfileblocks /
hdfs dfsadmin -report
```
###### HIVE
```
# базовый тест запросов 

hive
show databases;
show tables in <db_name>;
select * from <db_name>.<table_name> limit 5;
describe formatted <db_name>.<table_name>;

# создание/удаление временной базы, таблицы 

create database test_hive_cluster_db location '/tmp/test_hive_cluster_db location';
create external table 'test_hive_cluster_table' ('path' string, 'rep' int) LOCATION 'hdfs://<cluster_name>/tmp/test_hive_cluster_db';
drop table test_hive_cluster_table;
drop database test_hive_cluster_db;
```
###### BEELINE
```
# запуск tez через beeline в очереди <queue>
# создание/удаление временной базы, таблицы 
beeline
beeline --hiveconf tez.queue.name=<queue_name>

show databases;
show tables in <db_name>;
select * from <db_name>.<table_name> limit 5;
describe formatted <db_name>.<table_name>;


create database test_beeline_cluster_db location '/tmp/test_beeline_cluster_db location';
create external table 'test_beeline_cluster_table' ('path' string, 'rep' int) LOCATION 'hdfs://<cluster_name>/tmp/test_beeline_cluster_db';
drop table test_beeline_cluster_table;
drop database test_beeline_cluster_db;

```
###### IMPALA
```
impala-shell 
show databases;
show tables;
select * from <db_name>.<table_name> limit 5;
```
###### SPARK-SHELL
```
spark-shell
spark.sql ("show databases").show
spark.sql ("show tables in <db_name>").show
spark.sql ("select * from <db_name>.<table_name>").show(5)

spark-submit -v --class org.apache.spark.examples.SparkPi --master yarn --queue root.default <path_jar> 100
```
###### HBASE
```
hbase hbck
hbase shell
status 'simple'

whoami

list
describe "table_name"
show_filters
count "table_name", cache=>10

create 'smoke_test', 'cf'
list 'smoke_test'
put 'smoke_test', 'row1', 'cf:a', 'value1'
scan 'smoke_test'
get 'smoke_test', 'row1'
disable 'smoke_test'
drop 'smoke_test'
list
exit


```
