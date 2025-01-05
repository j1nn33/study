
#### Сбор логов с кластера ( отправка логов в NFS )
```
    - описание 
    - fluentbit                 
    - fluend                    
    - отправка логов в NFS      ./K8S/infra/ELK/to_NFS/to_NFS.md  
```
###### описание
```
Сбор логов с кластера на рисунке ./K8S/infra/ELK/image/logs.jpg

fluend  - роутер логв, куда скидываю все логи fluentbit, потоим эти логи парсятся\модифицируются 
          и отправляются в kafka\elastic
        - может быть несколько экземпляров для каждого типа логов   

конфигурационный файл    - ./K8S/infra/ELK/to_NFS/fluentd-cm.yaml
конфигурация pvc         - ./K8S/infra/ELK/to_NFS/fluentd-pvc.yaml
deployment               - ./K8S/infra/ELK/to_NFS/fluentd.yaml

конфигурационный файл
   - задает конфигурацию для тегирования логов 
   - match отбирает логи помеченные соответсвующим тегом (два исходящих потоков логов)

конфигурация pvc
   - ReadWriteMany позволяет подключаться нескольким подам к этому стораджу 
     например запускам неколько экземпляров fluend для разного типа логов 


ds-fluentbit   - daemonset который работае на каждой ноде собирает логи с каждой ноды каластера

конфигурационный файл    - ./K8S/infra/ELK/to_NFS/fluentbit-cm.yaml
deployment               - ./K8S/infra/ELK/to_NFS/flunetbit.yaml

конфигурационный файл
   - INPUT  - какие логи мы забираем с нод /var/log/containers/
   - Tag    - тегирутем логи (далее используется fluend при match логов)
   - OUTPUT - fluentd-forward 24224 (см ./K8S/infra/ELK/to_NFS/fluentd.yaml)

deployment
   - роли необходимы чтобы собирать логи из k8s
   - volume типа hostpath необходимо дать доступ к файловой системе хоста 
   - tolerations для размещения на всех нодах
```

###### Установка 
```bash 
# наличие namespace logging   ./K8S/infra/utils/namespace.yaml
kubectl apply -f namespace.yaml

# наличие priority-class   ./K8S/infra/utils/priority-class.yaml
kubectl apply -f priority-class.yaml

# в примере рассматривается отправка логов в NFS 
kubectl apply -f 01_fluentd-cm.yaml

# PVS создан см ./K8S/infra/NFS/readme.md
kubectl apply -f 02_fluentd-pvc.yaml
kubectl -n logging get pvc

# NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          VOLUMEATTRIBUTESCLASS   AGE
# fluentd-router-pvc   Bound    pvc-97e8d064-01c3-4b26-bb63-8f91e17eb580   5Gi        RWX            managed-nfs-storage   <unset>                 66d

# логи лежат на сервере NFS /var/nfs-disk/auto-pv/logging-fluentd-router-pvc

kubectl apply -f 03_fluentd.yaml
# смотрим в логах пода, что конфиг подцепился  using configuration file: <ROOT>

kubectl apply -f 04_fluentbit-cm.yaml

kubectl apply -f 05_fluentbit.yaml

# daemonset.apps/fluent-bit created
# смотрим логи пода 
# смотрим логи на сервере NFS /var/nfs-disk/auto-pv/logging-fluentd-router-pvc
#      - kube-system   - логи pod k8s 
#      - syslog        - логи хостов linux
#      - kubelet логи  - в логах системы /var/log/messages
```

   




