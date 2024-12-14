#### Архитектура
#### Сбор логов с кластера 
```
    - где живут логи 
    - fluentbit      ./K8S/infra/ELK/fluentbit.md
    - fluend         ./K8S/infra/ELK/fluend.md
    
    Установка
```
#### Сбор логов со сторны приклада 

###### Архитектура
```
Типичная архитектура сбора логов на рисунке ./K8S/infra/ELK/image/arch.jpg

    - fluentbit
    - kafka         
    - vector/logstash
    - opensearch 

Описание ./ELK/arch.md
  - назначение нод
  - жизненый цикл данных
  - масштабирование 

```

###### Сбор логов с кластера 
```
Где живут логи 

#      - kube-system   - логи pod k8s 
#      - syslog        - логи хостов linux
#      - kubelet логи  - в логах системы /var/log/messages
#      - /var/log/containers/<name_pod>_<name_namespace>_*.log
#      - /var/log/containers/*_kube-system_*.log

Сбор логов с кластера на рисунке ./K8S/infra/ELK/image/logs.jpg

fluend  - роутер логв, куда скидываю все логи fluentbit, потоим эти логи парсятся\модифицируются 
          и отправляются в kafka\elastic
        - может быть несколько экземпляров для каждого типа логов   

конфигурационный файл    - ./K8S/infra/ELK/source/fluentd-cm.yaml
конфигурация pvc         - ./K8S/infra/ELK/source/fluentd-pvc.yaml
deployment               - ./K8S/infra/ELK/source/fluentd.yaml

конфигурационный файл
   - задает конфигурацию для тегирования логов 
   - match отбирает логи помеченные соответсвующим тегом (два исходящих потоков логов)

конфигурация pvc
   - ReadWriteMany позволяет подключаться нескольким подам к этому стораджу 
     например запускам неколько экземпляров fluend для разного типа логов 


ds-fluentbit   - daemonset который работае на каждой ноде собирает логи с каждой ноды каластера

конфигурационный файл    - ./K8S/infra/ELK/source/fluentbit-cm.yaml
deployment               - ./K8S/infra/ELK/source/flunetbit.yaml

конфигурационный файл
   - INPUT  - какие логи мы забираем с нод /var/log/containers/
   - Tag    - тегирутем логи (далее используется fluend при match логов)
   - OUTPUT - fluentd-forward 24224 (см ./K8S/infra/ELK/source/fluentd.yaml)

deployment
   - роли необходимы чтобы собирать логи из k8s
   - volume типа hostpath необходимо дать доступ к файловой системе хоста 
   - tolerations для размещения на всех нодах

Установка 

# наличие namespace logging   ./K8S/infra/utils/namespace.yaml
kubectl apply -f namespace.yaml

# наличие priority-class   ./K8S/infra/utils/priority-class.yaml
kubectl apply -f priority-class.yaml

kubectl apply -f fluentd-cm.yaml

# PVS создан см ./K8S/infra/NFS/readme.md
kubectl apply -f fluentd-pvc.yaml
kubectl -n logging get pvc
# NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          VOLUMEATTRIBUTESCLASS   AGE
# fluentd-router-pvc   Bound    pvc-97e8d064-01c3-4b26-bb63-8f91e17eb580   5Gi        RWX            managed-nfs-storage   <unset>                 66d

# логи лежат на сервере NFS /var/nfs-disk/auto-pv/logging-fluentd-router-pvc

kubectl apply -f fluentd.yaml
# смотрим в логах пода, что конфиг подцепился  using configuration file: <ROOT>

kubectl apply -f fluentbit-cm.yaml

kubectl apply -f fluentbit.yaml
# daemonset.apps/fluent-bit created
# смотрим логи пода 
# смотрим логи на сервере NFS /var/nfs-disk/auto-pv/logging-fluentd-router-pvc
#      - kube-system   - логи pod k8s 
#      - syslog        - логи хостов linux
#      - kubelet логи  - в логах системы /var/log/messages


   

```
###### Сбор логов со сторны приклада 
```
```
######






