## ingress                                    
######    - ingress controller (теория)       
######    - ingress controller (Over a NodePort Service)          
######    - пример ingress (Over a NodePort Service)  
######    - ingress controller (Via the host network)       
######    - пример ingress (Via the host network)         
######    - DEBUG


#### ingress controller (теория)
```
https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/

# оригинальный 
  https://kubernetes.github.io/ingress-nginx/deploy/

# установка Bare-metal considerations
  https://kubernetes.github.io/ingress-nginx/deploy/baremetal/
# 
# в примерах будем устанавливать в 2 режимах  
#  - Over a NodePort Service 
     https://kubernetes.github.io/ingress-nginx/deploy/baremetal/#over-a-nodeport-service
#  - Via the host network
     https://kubernetes.github.io/ingress-nginx/deploy/baremetal/#via-the-host-network
# 
# Over a NodePort Service 
# картинка ./K8S/tasks/kryukov/network/ingress/base.jpg
# при такой схеме запросы будут попадать случайно на ingress controller

# Via the host network
# картинка ./K8S/tasks/kryukov/network/ingress/goal2.jpg
# - под выставляется напрямую в интернет
# - под не попадает под сетевые политики 
```
#### ingress controller (Over a NodePort Service) 
```
# целевая схема реализации 
# картинка ./K8S/tasks/kryukov/network/ingress/goal1.jpg
# NodePort все запросы будут направляться только на свой ingress controller, если он упадет то конекты пойдут на другой 
# для этого надо чтобы NodePort открывался только на ноде где есть ingress controller и отсылал запросы только на этот ingress controller

# описание структуры ingress
#  - оригинальная  ./K8S/tasks/kryukov/network/ingress/links_base.jpg
#  - целевая       ./K8S/tasks/kryukov/network/ingress/links_nodeport.jpg

# установка оригинала
https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal-clusters
https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/baremetal/deploy.yaml или ()./K8S/tasks/kryukov/network/ingress/deploy.yaml)
# исходник устанавливает вариант (картинка ./K8S/tasks/kryukov/network/ingress/base.jpg)

# процесс дорабоки до целевой схемы nodeport-ingress-controller.yaml
# Берем исходник и дорабатвает до целевой схемы  
https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.11.1/deploy/static/provider/baremetal/deploy.yaml

# процесс дорабоки nodeport-ingress-controller.yaml (./K8S/tasks/kryukov/network/ingress/nodeport-ingress-controller.yaml)

# Добавления для отправки логов ELK в json и для проксирования на 3 уровне 
https://kubernetes.github.io/ingress-nginx/user-guide/exposing-tcp-udp-services/
# по умолчанию только http трафик на 7 уровне 
# данные конфиг мапы подключат проксирование трафика на 3 урвне или использовать haproxy

# kind: ConfigMap  - для 3 уровня 
#   name: tcp-services
#   name: udp-services
---
apiVersion: v1
data:
  allow-snippet-annotations: "false"
kind: ConfigMap
metadata:
  labels:
    app.kubernetes.io/component: controller
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/part-of: ingress-nginx
    app.kubernetes.io/version: 1.11.1
  name: ingress-nginx-controller
  namespace: ingress-nginx
data:
  use-forwarded-headers: "true"
  use-gzip: "false"
  log-format-escape-json: "true"
  log-format-upstream: '{"time": "$time_iso8601", "remote_addr": "$proxy_protocol_addr", "x-forward-for": "$proxy_add_x_forwarded_for", "request_id": "$req_id", "remote_user": "$remote_user", "bytes_sent": $bytes_sent, "request_time": $request_time, "status":$status, "vhost": "$host", "request_proto": "$server_protocol", "path": "$uri", "request_query": "$args", "request_length": $request_length, "duration": $request_time,"method": "$request_method", "http_referrer": "$http_referer", "http_user_agent": "$http_user_agent", "namespace": "$namespace", "ingress_name": "$ingress_name", "service_name": "$service_name", "service_port": "$service_port" }'
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: tcp-services
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/component: controller
data:

---
kind: ConfigMap
apiVersion: v1
metadata:
  name: udp-services
  namespace: ingress-nginx
  labels:
    app.kubernetes.io/name: ingress-nginx
    app.kubernetes.io/instance: ingress-nginx
    app.kubernetes.io/component: controller
data:

---
# + service для 3 уровня 
---
name: ingress-nginx-controller
  - appProtocol: http
    name: http
    port: 80
  # явное указание какой порт выставлять (он не дожен быть занят во всем каластере)
    nodePort: 30080
    protocol: TCP
    targetPort: http
  - appProtocol: https
    name: https
    port: 443
    # явное указание какой порт выставлять (он не дожен быть занят во всем каластере)
    nodePort: 30443
  
  # Открываем порты только на тех машинах, где находятся
  # поды контроллера
  externalTrafficPolicy: Local

Deployment
  # ставим две реплики
  replicas: 2
  
  nodeSelector:
    # обязательно пометить ноды, на которых может быть
    # установлен контроллер
    ingress-nginx-node: enable

   # добавлены конфиги для tcp и udp сервисов
        - --udp-services-configmap=$(POD_NAMESPACE)/udp-services 
        - --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
        # Задаём класс, который можно указывать при 
        # определении ingress это необходимо когда на кластере есть несколько ingress-controller 
        # в этом случае при создании ingress (ingressClassName: nginx) явно указываем на какой завязываться ingress-controller 
        #  - --ingress-class=nginx
        # Определяет namespace ingress которого будет обслуживать
        # контроллер. Если пустой, то отслеживаются все namespaces 
        # - --watch-namespace=my-project-namespace
---

# Запуск и проверка
# сделать лейбы на ноды, чтобы igress-controller запускался только на них 

kubectl label nodes worker1.kube.local ingress-nginx-node=enable
kubectl label nodes worker2.kube.local ingress-nginx-node=enable

# запустить деплоймент (репликасет сделать 1 для тестового кластера)

kubectl apply -f nodeport-ingress-controller.yaml

# посмотеть поды в namespace  ingress-nginx

kubectl get pods -n ingress-nginx
# NAME                                       READY   STATUS      RESTARTS        AGE
# ingress-nginx-admission-create-nsf45       0/1     Completed   0               28d    - 
# ingress-nginx-admission-patch-fz69q        0/1     Completed   1               28d    -
# ingress-nginx-controller-f7587f845-g5wq9   1/1     Running     2 (6h36m ago)   28d    - сам ingress-nginx-controller

# Посмотреть порты на которых висит ingress-controllre 30180  30443
kubectl get service -ALL | grep ingress-nginx

# ingress-nginx          ingress-nginx-controller             NodePort    10.233.53.170   <none>        80:30180/TCP,443:30443/TCP   63m
# ingress-nginx          ingress-nginx-controller-admission   ClusterIP   10.233.62.16    <none>        443/TCP                      63m

# В логах контейнера ingress-nginx-controller можно увидеть что подхвачены configmap
#
# Event(v1.ObjectReference{Kind:"ConfigMap", Namespace:"ingress-nginx", Name:"ingress-nginx-controller", UID:"ef56ee62-6158-4e3b-a6ad-3060b3df1be8", APIVersion:"v1", ResourceVersion:"397351", FieldPath:""}): type: Normal' reason: 'CREATE' ConfigMap ingress-nginx/ingress-nginx-controller
# Event(v1.ObjectReference{Kind:"ConfigMap", Namespace:"ingress-nginx", Name:"tcp-services", UID:"18b7db30-26fd-4e5e-b893-2a9478eaa1ac", APIVersion:"v1", ResourceVersion:"397352", FieldPath:""}): type: 'Normal' reason: 'CREATE' ConfigMap ingress-nginx/tcp-services
# Event(v1.ObjectReference{Kind:"ConfigMap", Namespace:"ingress-nginx", Name:"udp-services", UID:"26c35cc3-67f2-4cbe-8979-11bac4f521db", APIVersion:"v1", ResourceVersion:"397353", FieldPath:""}): type: 'Normal' reason: 'CREATE' ConfigMap ingress-nginx/udp-services

# Смотрим сервисы 
# kubectl get service -n ingress-nginx
# NAME                                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# ingress-nginx-controller             NodePort    10.233.53.170   <none>        80:30180/TCP,443:30443/TCP   28d
# ingress-nginx-controller-admission   ClusterIP   10.233.62.16    <none>        443/TCP                      28d

# Попасть к сервисам с наружи можно по этим ссыкам
http://192.168.1.171:30180/
https://192.168.1.171:30443/
```
####  пример ingress controller (Over a NodePort Service)   

```
# Запускаем следующий ingress для примера (Openresty)
# выставляем наружу сервис ./K8S/tasks/kryukov/local_volumes/prepare-cluster-volume.yaml
# сервис для               ./K8S/tasks/kryukov/local_volumes/12_openresty_projected.yaml 
# ingress                  ./K8S/tasks/kryukov/network/ingress/openresty.yml
kubectl apply -f openresty.yml

# cat openresty.yml
# apiVersion: networking.k8s.io/v1
# kind: Ingress
# metadata:
#   name: access-openresty            
#   namespace: volumes-sample
# spec:
#   ingressClassName: nginx    - имя ingressClass указывали  ./K8S/tasks/kryukov/network/ingress/nodeport-ingress-controller.yaml - --ingress-class=nginx (строка 468)
#   rules:
#   - http:
#       paths:
#       - path: /
#         pathType: Prefix
#         backend:
#           service:
#             name: openresty-srv
#             port:
#               number: 80




# При проблемах смотрим логи ingress controller

```
#### ingress controller (Via the host network) 
```
ingress-controller садиться сетевой loopback interface хостовой ноды

архитектура goal3
на картинке изображены 2 ингресс контролера (для кластера это нормально):
   - ingress controller nodeport(ingress-class=nginx) 
   - ingress controller HostNetwork(ingress-class=nginx-host) 
   - при такой схеме ingress нужно явно указывать на какой ingress controller завязываться (ingress-class=nginx или ingress-class=nginx-host)
в нашем случае конролер сядет на попорты 280, 2443

плюсы решения
    - можно посадить конртолер на 80, 443 порты, если они свободны на хосте (ingress controller nodeport сделать без танцев не получиться - делать так bad practics)  
    - не нужно делать перед ним сервис
    - нет NAT преобразований  	
минусы решения
    - если его ломанут, то попадают на loopback interface хостовой ноды

----------------
манифест ingress-controller HostNetwork на основе манифеста ingress controller nodeport
измения описаны в host-ingress-controller.yaml

для работы требуется теже сущности что и nodeport-ingress-controller.yaml
(тк они созданы и расктаны в  nodeport-ingress-controller.yaml то их раскатывать заново не требутеся )

сущности которые уже расктаны и если host-ingress-controller.yaml будте подниматься отдельно то необходимо их применить 

- Namespace
    name: ingress-nginx
- ServiceAccount
    name: ingress-nginx
    name: ingress-nginx-admission
- ClusterRole
    name: ingress-nginx
    name: ingress-nginx-admission
- ClusterRoleBinding
    name: ingress-nginx
    name: ingress-nginx-admission
- Role
    name: ingress-nginx
    name: ingress-nginx-admission
- RoleBinding
    name: ingress-nginx
    name: ingress-nginx-admission
- Service
    name: ingress-nginx-controller
    name: ingress-nginx-controller-admission
- ValidatingWebhookConfiguration
- Job
- ServiceAccount

измения  
- ConfigMap
  имя, label
  удалено (тк нет балансировщика и клиенты идут на него напрямую)
   - use-forwarded-headers: "true"
   - use-gzip: "false

- Deployment
  spec:
      dnsPolicy: ClusterFirst
      # Вешаем поды непосредственно на сетевые интерфейсы node. 
      # --->>>> В том числе и на loopback!!!!! <<<< -----
      hostNetwork: true
	  
  args:
      - --ingress-class=nginx-host
      - --configmap=$(POD_NAMESPACE)/ingress-nginx-controller-host
      # Определяет namespace ingress которого будет обслуживать
      # контроллер. Если пустой, то отслеживаются все namespaces
      # - --watch-namespace=my-project-namespace
	  
	  # убедиться что порты на этих нода свободны
      - --http-port=280  
      - --https-port=2443
 
 убраны 
    # добавлены конфиги для tcp и udp сервисов
    # --tcp-services-configmap=$(POD_NAMESPACE)/tcp-services
    # --udp-services-configmap=$(POD_NAMESPACE)/udp-services


# Запуск
kubectl apply -f host-ingress-controller.yaml

# Для тестового кластера replicaset=1 
kubectl -n ingress-nginx get  pods
# NAME                                             READY   STATUS      RESTARTS        AGE
# ingress-nginx-admission-create-nsf45             0/1     Completed   0               34d
# ingress-nginx-admission-patch-fz69q              0/1     Completed   1               34d
# ingress-nginx-controller-f7587f845-5wt74         1/1     Running     1 (5d15h ago)   6d17h
# ingress-nginx-controller-host-6756b9c66c-wmp76   1/1     Running     0               5m7s


```
#### пример ingress controller (Via the host network)        
```
# Запускаем следующий ingress для примера (Openresty)

kubectl apply -f openresty_ingress_host.yml

Отличия от передыдущего openresty.yml

# cat openresty_ingress_host.yml
name: access-openresty-host
 spec:
  ingressClassName: nginx-host    - имя ingressClass указывали  ./K8S/tasks/kryukov/network/ingress/nodeport-ingress-controller.yaml - --ingress-class=nginx (строка 468)

http://192.168.1.171:280/
https://192.168.1.171:2443/

# Проверка портов 
netstat -tulpen | grep 80
# tcp        0      0 0.0.0.0:280             0.0.0.0:*               LISTEN      101        395404     66732/nginx: master
# tcp6       0      0 :::280                  :::*                    LISTEN      101        395395     66732/nginx: master

netstat -tulpen | grep 443
# tcp        0      0 0.0.0.0:2443            0.0.0.0:*               LISTEN      101        395410     66732/nginx: master
# tcp6       0      0 :::2443                 :::*          

# При проблемах смотрим логи ingress controller

"Configuration changes detected, backend reload required"
"New leader elected" identity="ingress-nginx-controller-f7587f845-2w4d7"
"Backend successfully reloaded"
"Initial sync, sleeping for 1 second"
Event(v1.ObjectReference{Kind:"Pod", Namespace:"ingress-nginx", Name:"ingress-nginx-controller-host-c4f6d77c9-7rvrv", UID:"8e624301-b5a2-48e2-a37e-0e9dedd21db6", APIVersion:"v1", ResourceVersion:"690321", FieldPath:""}): type: 'Normal' reason: 'RELOAD' NGINX reload triggered due to a change in configuration
{"time": "2024-09-22T11:01:23+00:00", "remote_addr": "", "x-forward-for": "192.168.1.37", "request_id": "907bbdacc44b8546632ba291358a696e", "remote_user": "", "bytes_sent": 129110, "request_time": 0.002, "status":200, "vhost": "192.168.1.171", "request_proto": "HTTP/2.0", "path": "/", "request_query": "", "request_length": 2062, "duration": 0.002,"method": "GET", "http_referrer": "", "http_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36", "namespace": "volumes-sample", "ingress_name": "access-openresty", "service_name": "openresty-srv", "service_port": "80" }

```

#### DEBUG
```
ingres(port 80)  ----> service (clusterIP:80)

ingress ссылается на service приложения 

Важно 
  указываем на какой ingress-controller вешается ingress
  annotations:  
    kubernetes.io/ingress.class: "nginx-host"  

ingress debug
- log ingress-controller
  идем в POD ingress-controller
  
# ЗАГРУЗКА И СТАРТ INGRESS в INGRESS-CONTROLLER  
	"successfully validated configuration, accepting" ingress="volumes-sample/access-openresty"
	"Found valid IngressClass" ingress="volumes-sample/access-openresty" ingressclass="nginx"
	"Configuration changes detected, backend reload required"
	Event(v1.ObjectReference{Kind:"Ingress", Namespace:"volumes-sample", Name:"access-openresty", UID:"ce0b9195-76e2-4cee-92d6-8886cb9ef237", APIVersion:"networking.k8s.io/v1", ResourceVersion:"655342", FieldPath:""}): type: 'Normal' reason: 'Sync' Scheduled for sync
	"Backend successfully reloaded"
	Event(v1.ObjectReference{Kind:"Pod", Namespace:"ingress-nginx", Name:"ingress-nginx-controller-f7587f845-5wt74", UID:"f135e38e-c412-484f-86fd-5e95dc49de38", APIVersion:"v1", ResourceVersion:"649774", FieldPath:""}): type: 'Normal' reason: 'RELOAD' NGINX reload triggered due to a change in configuration

# ЛОГИ ДОСТПУПА К ПОДУ ПРИЛОЖЕНИЯ в формате json как определяли выше для разбора в ELK

	{"time": "2024-09-22T07:09:28+00:00", "remote_addr": "", "x-forward-for": "192.168.1.37", "request_id": "f8e9ccc66186124a550276e1f5b78f63", "remote_user": "", "bytes_sent": 129110, "request_time": 0.012, "status":200, "vhost": "192.168.1.171", "request_proto": "HTTP/2.0", "path": "/", "request_query": "", "request_length": 2065, "duration": 0.012,"method": "GET", "http_referrer": "", "http_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36", "namespace": "volumes-sample", "ingress_name": "access-openresty", "service_name": "openresty-srv", "service_port": "80" }

```