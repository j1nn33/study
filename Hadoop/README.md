#### install single node 
#### asnible_smoke_test 
####
####


Hadoop

| INTEGRATION      |  DATA ACCESS       |  SECURITY         | OPERATION    |
|-----------------:|:------------------:|:-----------------:|:-------------|
| sqoop            | Map Reduse   TEZ   |  kerberos client  | Amabry       |
| WebHDFS          |             (Dag)  |                   |              |
|                  |                    |                   |              |
| livy             | Hive        Hbace  |  Ranger Plugins   | Zookeeper    |       
| (Spark rest)     | Solr        Spark  |                   |              |
|                  |                    |                   |              |
| Hue              |       YARN         |                   |    Oozie     |
|                  |                    |                   |              |
|                  |   HDFS OZONE       |                   |              |



###### install single node 
```
./study/Ansible/tasks/hadoop_single_node
```
###### asnible_smoke_test
```
./study/Ansible/tasks/smoke_test_for_hadoop
```