## ingress                                    
######    - ingress controller (теория)       
######    - ingress controller (Over a NodePort Service)          
######    - пример ingress (Over a NodePort Service)  
######    - ingress controller (Via the host network)       
######    - пример ingress (Via the host network)         

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
        # определении ingress
        # - --ingress-class=my-test-ingress
        # Определяет namespace ingress которого будет обслуживать
        # контроллер. Если пустой, то отслеживаются все namespaces
        # - --watch-namespace=my-project-namespace
---

```
####  пример ingress controller (Over a NodePort Service)   
```
# сделать лейбы на ноды, чтобы igress-controller запускался только на них 

kubectl label nodes worker1.kube.local ingress-nginx-node=enable
kubectl label nodes worker2.kube.local ingress-nginx-node=enable

# запустить деплоймент (репликасет сделать 1 для тестового кластера)

kubectl apply -f nodeport-ingress-controller.yaml

# Посмотреть порты  
kubectl get service -ALL | grep ingress-nginx

# ingress-nginx          ingress-nginx-controller             NodePort    10.233.53.170   <none>        80:30180/TCP,443:30443/TCP   63m
# ingress-nginx          ingress-nginx-controller-admission   ClusterIP   10.233.62.16    <none>        443/TCP                      63m



http://192.168.1.171:30180/
https://192.168.1.171:30443/


```
#### ingress controller (Via the host network) 
```

```
#### пример ingress controller (Via the host network)        
```

```