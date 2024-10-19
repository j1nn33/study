## ResourceQuota                             
#####  Теория
#####  Типы квот
###### Вычислительные  
###### Хранения  
###### Количество объектов  
###### Информация о квотах
###### Пример

#####  Теория 
```
ResoqurceQuota определяет ограничения на namespace. 
  - Ограничивает количество объектов, создаваемых в namespace, по типу.
  - Ограничевает общий объем вычислительных ресурсов.

Квоты работаю следующим образом:
  - Создается ResourceQuota в namespace.
  - Пользователи создают объекты в namespace. 
  - Система отслеживает, не превышают ли запрошенные ресурсы лимиты, описанные в квотах.
    Если создание нового ресурса превышает квоту, API сервер возвращает 403-ю ошибку (FORBIDDEN)
    с сообщением о том, какие квоты были превышены.

Если в namespace включена квота на вычислительные ресурсы: cpu и memory. 
В создаваемых пользователем ресурсах должны быть явно описаны лимиты. 
Если лимиты не описаны, система отклонит создание новых ресурсов. 
Для избегания подобной ситуации администратор должен устанавливать LimitRanger на namespace.
```
##### Типы квот

###### Вычислительные
```
  - limits.cpu
  - limits.memory
  - requests.cpu
  - requests.memory
```
###### Хранения
```
  - requests.storage
  - persistentvolumeclaims
  - .storageclass.storage.k8s.io/requests.storage
  - .storageclass.storage.k8s.io/persistentvolumeclaims
```
###### Количество объектов
```
  - configmaps
  - pods
  - replicationcontrollers
  - resourcequotas
  - services
  - services.loadbalancers
  - services.nodeports
  - secrets
```
##### Информация о квотах
```
kubectl -n <name_namespace> describe quota
kubectl -n <name_namespace> describe limitrange
```    
###### Пример
```
# Создание тестового namespace
kubectl apply -f 01-ns.yaml
kubectl -n q-test describe quota
# No resources found in q-test namespace.

# Определение квоты (применяется к namespace)
# по ./K8S/tasks/kryukov/resource_quota/02-quota.yaml
# hard квоты те которые нельзя привысить
# services.nodeports: "0"                        - 0 значит данный тип сервисов создавать нельзя
# anaged-nfs-storage.storageclass.storage.k8s.io - уже был создан заранее ./K8S/tasks/kryukov/pv_volumes_dynamic

kubectl apply -f 02-quota.yaml

kubectl -n q-test describe quota
# Name:                                                                   q-test-quota
# Namespace:                                                              q-test
# Resource                                                                Used  Hard
# --------                                                                ----  ----
# limits.cpu                                                              0     2
# limits.memory                                                           0     2Gi
# managed-nfs-storage.storageclass.storage.k8s.io/persistentvolumeclaims  0     1
# managed-nfs-storage.storageclass.storage.k8s.io/requests.storage        0     8Gi
# persistentvolumeclaims                                                  0     2
# pods                                                                    0     2
# requests.cpu                                                            0     200m
# requests.memory                                                         0     200Mi
# services                                                                0     2
# services.nodeports                                                      0     0

# При добавлении квот, рекомендуется определить LimitRange.
# необходимо в случае если квоту включили, а пользователь не описывает ус ебя лимиты, то ресур не создается 
# Для избегания подобной ситуации администратор должен устанавливать LimitRanger на namespace.
# LimitRanger - определяте лимиты в подах по умолчанию, если они не заданы
kubectl apply -f 03-limitrange.yaml

kubectl -n q-test describe limitrange
# Name:       q-test-lr
# Namespace:  q-test
# Type        Resource  Min  Max  Default Request  Default Limit  Max Limit/Request Ratio
# ----        --------  ---  ---  ---------------  -------------  -----------------------
# Container   cpu       -    2    100m             100m           -
# Container   memory    -    2Gi  256Mi            512Mi          -

# раскатка приложения с 3 репликами, тогда как в лимитах определено 2
kubectl apply -f 04-deployment.yaml

# вывод ошибок не дает запустилось только 2 pod

kubectl get deployment -n q-test
# NAME        READY   UP-TO-DATE   AVAILABLE   AGE
# openresty   2/3     2            2           7m43s

kubectl get events -n q-test

kubectl get events -n q-test
# Error creating: pods "openresty-c9dbdd948-2kwdn" is forbidden: exceeded quota: q-test-quota, requested: pods=1,requests.cpu=100m,requests.memory=100Mi, used: pods=2,requests.cpu=200m,requests.memory=200Mi, limited: pods=2,requests.cpu=200m,requests.memory=200Mi


# Квота на сервис который запрещает создание в namespace сервисов типа nodeports

kubectl apply -f 06-service_node_port.yaml
# Error from server (Forbidden): error when applying patch:
# services "openresty" is forbidden: exceeded quota: q-test-quota, requested: services.nodeports=1, used: services.nodeports=0, limited: services.nodeports=0

# Квота на хранение 
kubectl apply -f 07-pvc.yaml
```