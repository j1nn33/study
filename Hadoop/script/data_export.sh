# /usr/bin/env bash
set +x

LOCAL_OUT_DIR=/root/1_task
HIVE_REPO_PATH=/data/test_db
BEELINE_RUN="beeline -u jdbc:hive2://192.168.1.151:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2"

echo $LOCAL_OUT_DIR
echo $HIVE_REPO_PATH
echo $BEELINE_RUN

## Если выполнение скриптов в beeline падает из-за доступов то попробовать через Hive

# Проверка доступности базового каталога с HIVE-данными

if $(hdfs dfs -test -d $HIVE_REPO_PATH);
then echo "Output path FOUND: $HIVE_REPO_PATH";
else echo "Output path NOT FOUND: $HIVE_REPO_PATH" & exit;
fi;

# Создание временного пути для выгрузки
echo "Crete temp location for data export"
hdfs dfs -mkdir -p $HIVE_REPO_PATH/temp_location_output_csv_raw

# Запуск скрипта выгрузки
echo "RUN the data export script"
$BEELINE_RUN --outputformat=csv2 --silent=false --showHeader=false --force -f export.hql > $LOCAL_OUT_DIR/output.csv 

# Загрузака CSV в hdfs
echo "Upload the exported CSV into HDFS";
hdfs dfs -copyFromLocal -f $LOCAL_OUT_DIR/output.csv $HIVE_REPO_PATH/temp_location_output_csv_raw/output.csv

# Запуск скрипта загрузки данных в 
echo "Run script to create the HIVE Parquet table from CSV"
$BEELINE_RUN --silent=false --force -f upload.hql --hivevar csv_path=$HIVE_REPO_PATH/temp_location_output_csv_raw

# убрать за собой 
#echo "REMOVE $LOCAL_OUT_DIR/output.csv";
#rm -f $LOCAL_OUT_DIR/output.csv
#echo "DROP the temp data export location from HDFS";
#hdfs dfs -rm -r $HIVE_REPO_PATH/temp_location_output_csv_raw