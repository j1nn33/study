#### Архитектура
#### Где живут логи 
#### Инфрастурктура 
```
   - NFS
   - Opensearch 
   - kafka

```
#### Сбор логов с кластера 
```
   - fluentbit                 ./K8S/infra/ELK/fluentbit.md
   - fluend                    ./K8S/infra/ELK/fluend.md
   - отправка логов в NFS      ./K8S/infra/ELK/to_NFS/to_NFS.md  
   - тестовое приложение       ./K8S/infra/ELK/test_app
``` 
#### Сбор логов со сторны приклада 

##### Архитектура
```
Типичная архитектура сбора логов на рисунке ./K8S/infra/ELK/image/arch.jpg
                                            ./K8S/infra/ELK/image/logs.jpg

    - fluentbit            - сборщик логов с нод кластера или с самих подов 
    - fluentd              - роутер логов (их может быть несколько)
    - kafka               
    - vector/logstash
    - opensearch 
```
##### Где живут логи 
```
#      - kube-system   - логи pod k8s 
#      - syslog        - логи хостов linux
#      - kubelet логи  - в логах системы /var/log/messages
#      - /var/log/containers/<name_pod>_<name_namespace>_*.log
#      - /var/log/containers/*_kube-system_*.log
```

##### Сбор логов с кластера 
```
Описаине примера отправки логов в хранилище NFS          ./K8S/infra/ELK/to_NFS/to_NFS.md 
Описаине примера отправки логов в ELK                    ./K8S/infra/ELK/to_ELK/to_ELK.md 

```
##### Сбор логов со сторны приклада 
```
   ./K8S/infra/ELK/from_app_log/README.md
```







