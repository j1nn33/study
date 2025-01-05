## fluend
##### Документация 
##### Решение 
##### Описание 
##### Установка  
##### Проверка

##### Документация 
```
fluend - роутер логв, куда скидываю все логи fluentbit, потоим эти логи парсятся\модифицируются и отправляются в kafka\elastic
```
##### Решение 
```
картинка  ./K8S/infra/ELK/image/logs.jpg
```
##### Описание 
```
Каталог манифестов    ./K8S/infra/ELK/k8s_fluentd

./K8S/infra/ELK/k8s_fluentd/01-fluentd-pvc.yaml        - PVC для хранения логов в NFS - PVS создан см ./K8S/infra/NFS/readme.md
./K8S/infra/ELK/k8s_fluentd/02-fluentd-cm.yaml         - конфигурационный файл fluentd 
./K8S/infra/ELK/k8s_fluentd/03-fluentd-deploy.yaml     - Deployment
./K8S/infra/ELK/k8s_fluentd/04-flunetd-service.yaml    - Service

```
```bash
# 02-fluentd-cm.yaml 
#---
#    - секция <source>                           - https://docs.fluentd.org/input/forward
#    <source> 
#      @type  forward        
#      port  24224                               - на каком порту слушает 
#    </source>
#
# куда отправлять логи  <match>                 - https://docs.fluentd.org/output
#
#    <match example-app.**>                     - какие теги отрабатывать  (* - один симовол  ** - все что угодно)
#      @type file                               - куда отправлять (в данном случае в файл) 
#      path /fluentd/log/example-app            - где будет находиться файл
#      append true                              - информация будет дописываться в конец файла (необходимо если несколько инсталяций fluentd)
#      <format>                                 - в каком формате сохранять
#        @type json
#      </format>
#      <buffer>                                 - буферизация https://docs.fluentd.org/buffer
#        @type memory                          
#---
#
# 03-fluentd-deploy.yaml 
#---
# image: fluent/fluentd:v1.18.0-debian-1.0     - версию приклада в файле берем из docker hub /fluend  https://hub.docker.com/search?q=fluentd
# Важно необходимо найти тот image который содержит необходимый модуль 
# Если на этой ноде есть pod c меткой fluentd-forward, то деплоить на эту ноду нельзя (чтобы на одной ноде не жило 2 пода )
#      affinity:
#        podAntiAffinity:                                 
#          requiredDuringSchedulingIgnoredDuringExecution:
#          - topologyKey: kubernetes.io/hostname
#            labelSelector:                               
#              matchLabels:                               
#                app: fluentd-forward           
#
#---


```
##### Установка  
```bash
kubectl apply -f 01-fluentd-pvc.yaml
kubectl apply -f 02-fluentd-cm.yaml
kubectl apply -f 03-fluentd-deploy.yaml
kubectl apply -f 04-flunetd-service.yaml

```
##### Проверка
```
```
