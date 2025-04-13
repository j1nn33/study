
##### ADMIN
```
hdfs dfs -setrep 2 /<name_dir_file>
hdfs dfs -du -h /
hadoop fs -rm -R -skipTrash /<name_dir_file> 





# найти не зареплецированные файлы 
hdfs fsck / | grep 'Under replicated' | awk -F':' '{print $1}'

# найти не зареплецированные файлы у установить фактор репликации 2
hdfs fsck / | grep 'Under replicated' | awk -F':' '{print $1}' >> <name_file>
for hdfsfile in cat <name_file>; do hadoop fs -setrep 2 $hdfsfile; done
```
#####  DISCP

# откуда куда 
hadoop discp hdfs<name_node_source>:8020/<path>/* hdfs<name_node_tagert>:8020/<path>/*

============
hdfs dfs -chown -R <name>:<name> /<name_dir>
============

HDFS - DEBUG LOGGING

HADOOP_ROOT_LOGGER=DEBUG,console hdfs dfs -ls /
HADOOP_ROOT_LOGGER=WARN,console hdfs dfs -ls /
```