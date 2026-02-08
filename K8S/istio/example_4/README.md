
#### ISTIO EXAMPLE

```
https://www.freecodecamp.org/news/learn-istio-manage-microservices/
https://github.com/rinormaloku/master-istio.git 

```
###### APP
```
SA-Frontend   — service serves the frontend; a React JavaScript application
SA-WebApp     — service handles queries for analyzing the sentiment of sentences
SA-Logic      — service performs sentiment analysis
SA-Feedback   — service records the user feedback about the accuracy of the analysis

# см pic_2.png

```

###### Run the Services on the Mesh

```bash
# Create a namespace and label it for automatic injection.
kubectl create ns demo 
kubectl label ns demo istio-injection=enabled
kubectl get namespace -L istio-injection
# demo                   Active   20s    enabled

# Switch the kubectl context to the demo namespace
kubectl config set-context --current --namespace=demo


git clone https://github.com/rinormaloku/master-istio.git 
cd master-istio

deploy the services
kubectl apply -f ./kube

kubectl get pods -n demo
# NAME                           READY     STATUS    RESTARTS   AGE
# sa-feedback-55f5dc4d9c-c9wfv   2/2       Running   0          12m
# sa-frontend-558f8986-hhkj9     2/2       Running   0          12m
# sa-logic-568498cb4d-2sjwj      2/2       Running   0          12m
# sa-logic-568498cb4d-p4f8c      2/2       Running   0          12m
# sa-web-app-599cf47c7c-s7cvd    2/2       Running   0          12m

kubectl get pods -n demo --show-labels=true

# Проверка что в контейнер приложения заехал istio как sidecar 
# Проверить в поде 
# kubectl describe pod <pod_name> -n <namespace_name>

kubectl describe pod sa-frontend-566756455d-wgqz2 -n demo

# istio-proxy:
#    Container ID:  containerd://96aa1443bd8ec02d2efcfa7b2aebe618e7cdcb928c0b3d809cd62e3b3faabca3
#    Image:         docker.io/istio/proxyv2:1.27.2
#    Image ID:      docker.io/istio/proxyv2@sha256:b00a23cb37e7b8e422b57e617c1bb7304955e368308b5c166e38f0444e0f5a08
#    Port:          15090/TCP
#    Host Port:     0/TCP
#    Args:
#      proxy
#      sidecar


kubectl get service -n demo
# NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)            AGE
# sa-feedback          ClusterIP   10.233.4.59     <none>        80/TCP             27h
# sa-frontend          ClusterIP   10.233.41.11    <none>        80/TCP             27h
# sa-logic             ClusterIP   10.233.38.131   <none>        80/TCP             27h
# sa-webapp            ClusterIP   10.233.19.29    <none>        80/TCP             27h


# Проверить доступность сервиса 
kubectl port-forward --address 0.0.0.0 service/sa-frontend 88:80
http://192.168.1.171:88/
#

```
###### Open the application to outside traffic

```bash
# configure the Istio ingress gateway
kubectl apply -f http-gateway.yaml -n demo

kubectl describe Gateway http-gateway

# Configure HTTP routing

#  By default, Istio creates a LoadBalancer service for a gateway. As we will access this gateway by a tunnel, we don’t need a load balancer.
# Change the service type to ClusterIP by annotating the gateway:

kubectl annotate gateway http-gateway networking.istio.io/service-type=ClusterIP --namespace=demo
# configures traffic routing within the mesh for all proxies and gateways.
# Paths matching exactly      /                     should be routed to SA-Frontend to get the Index.html
# Paths prefixed with         /static/*             should be routed to SA-Frontend to get any static files needed by the frontend, like Cascading Style Sheets and JavaScript files.
# Paths that match the regex  '^.*\.(ico|png|jpg)$' should be routed to SA-Frontend.

kubectl apply -f vs-route-ingress.yaml
kubectl describe HTTPRoute sa-external-services -n demo

kubectl port-forward --address 0.0.0.0 service/http-gateway-istio 8080:80
kubectl port-forward -n demo svc/http-gateway-istio --address 0.0.0.0 8080:80
http://localhost:8080/
http://192.168.1.171:8080
 
```
###### Observability
```bash
# Prometheus  for collecting metrics
# Grafana     for visualizing those
# Jaeger      for snitching traces
# Kiali       brings all telemetry data together

kubectl get svc -n istio-system
# NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                                          AGE
# grafana            ClusterIP   10.233.39.70    <none>        3000/TCP                                         103d
# istiod             ClusterIP   10.233.60.184   <none>        15010/TCP,15012/TCP,443/TCP,15014/TCP            103d
# jaeger-collector   ClusterIP   10.233.30.185   <none>        14268/TCP,14250/TCP,9411/TCP,4317/TCP,4318/TCP   103d
# kiali              ClusterIP   10.233.3.216    <none>        20001/TCP,9090/TCP                               103d
# loki               ClusterIP   10.233.13.117   <none>        3100/TCP,9095/TCP                                103d
# loki-headless      ClusterIP   None            <none>        3100/TCP                                         103d
# loki-memberlist    ClusterIP   None            <none>        7946/TCP                                         103d
# prometheus         ClusterIP   10.233.38.209   <none>        9090/TCP                                         103d
# tracing            ClusterIP   10.233.30.211   <none>        80/TCP,16685/TCP                                 103d
# zipkin             ClusterIP   10.233.32.226   <none>        9411/TCP                                         103d


# grafana
#./istio-1.27.2/bin/istioctl dashboard grafana

istioctl dashboard grafana
kubectl port-forward --address 0.0.0.0 -n istio-system svc/grafana 3000:3000
http://192.168.1.171:3000

# istioctl dashboard jaeger
# http://localhost:16686

kubectl port-forward --address 0.0.0.0 -n istio-system svc/tracing 16686:80
#Forwarding from 0.0.0.0:16686 -> 16686
http://192.168.1.171:16686


istioctl dashboard kiali
kubectl port-forward --address 0.0.0.0 -n istio-system svc/kiali 20001:20001
http://192.168.1.171:20001/kiali 


# Без полезной нагрузки pic_kiali_1.png
# С полезной нагрузкой  pic_kiali_2.png

```




###### generate traffic
```bash
#!/bin/bash
while true; do \
  curl -i http://192.168.1.171:8080/sentiment \
  -H "Content-type: application/json" \
  -d '{"sentence": "I love yogobella"}'; \
  sleep .$RANDOM; done

```

###### LOG
```

[2026-02-01T16:29:24.710Z] "GET /static/js/main.f7659dbb.js HTTP/1.1"                      200             -                via_upstream            -                                 "-"                                    0                 279879       0         0                                      "10.233.66.16"             "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36" "8fcedd10-23a4-9b4d-8caa-ade8a92a66a8" "192.168.1.171:8080"      "10.233.66.32:80"  inbound|80||        127.0.0.6:40305         10.233.66.32:80            10.233.66.16:0              outbound_.80_._.sa-frontend.demo.svc.cluster.local default
"[%START_TIME%]           \"%REQ(:METHOD)% %REQ(X-ENVOY-ORIGINAL-PATH?:PATH)% %PROTOCOL%\" %RESPONSE_CODE% %RESPONSE_FLAGS% %RESPONSE_CODE_DETAILS% %CONNECTION_TERMINATION_DETAILS% \"%UPSTREAM_TRANSPORT_FAILURE_REASON%\" %BYTES_RECEIVED% %BYTES_SENT% %DURATION% %RESP(X-ENVOY-UPSTREAM-SERVICE-TIME)% \"%REQ(X-FORWARDED-FOR)%\" \"%REQ(USER-AGENT)%\"                                                                                              \"%REQ(X-REQUEST-ID)%                  \" \"%REQ(:AUTHORITY)%\" \"%UPSTREAM_HOST%\" %UPSTREAM_CLUSTER% %UPSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_LOCAL_ADDRESS% %DOWNSTREAM_REMOTE_ADDRESS% %REQUESTED_SERVER_NAME%                            %ROUTE_NAME%\n"

```

###### A/B Testing
```
we have two versions of an application
deploy a second version of the frontend (a green button instead of the white one)
https://github.com/rinormaloku/istio-mastery

Манифест deployment для «зелёной версии» отличается в двух местах:
Образ основан на ином теге — istio-green,
Pod'ы имеют лейбл version: green.

оба deployment'а имеют лейбл app: sa-frontend, запросы, маршрутизируемые виртуальным сервисом sa-external-services на сервис sa-frontend, будут перенаправлены на все его экземпляры и нагрузка распределится посредством алгоритма round-robin
см pic_4.png

Посмотреть измения можно на pic_3.png (менятся один файл)
Посмотреть на мониторинге  pic_mon_1.png

Без полезной нагрузки pic_kiali_1.png
С полезной нагрузкой  pic_kiali_2.png
```
```bash
kubectl apply -f  ./K8S/istio/example_4/source/kube/ab-test/sa-frontend-green-deployment.yaml -n demo
```

```bash
# При такой балансировке 
# на новом приложении файлы отличаются 
# index.html, запрашивающий одну версию статических файлов, может быть отправлен балансировщиком нагрузки на pod'ы,
# имеющие другую версию, где, по понятным причинам, таких файлов не существует.

$ curl --silent http://192.168.1.171:8080/ | tr '"' '\n' | grep main
/static/css/main.c7071b22.css
/static/js/main.059f8e9c.js
$ curl --silent http://192.168.1.171:8080/ | tr '"' '\n' | grep main
/static/css/main.f87cd8c9.css
/static/js/main.f7659dbb.js



для того, чтобы приложение заработало, нам необходимо поставить ограничение: 
«та же версия приложения, что отдала index.html, должна обслужить и последующие запросы».

# Используем непротиворечивой балансировки нагрузки на основе хэшей (Consistent Hash Loadbalancing). 
# В этом случае запросы от одного клиента отправляются в один и тот же экземпляр бэкенда, 
# для чего используется предопределённое свойство — например, HTTP-заголовок. Реализуется с помощью DestinationRules.

# в Destination Rules мы можем настроить балансировку нагрузки так, чтобы использовались непротиворечивые 
# хэши и гарантировались ответы одного и того же экземпляра сервиса одному и тому же пользователю

kubectl apply -f ./K8S/istio/example_4/source/kube/ab-test/destinationrule-sa-frontend.yaml -n demo
# destinationrule.networking.istio.io/sa-frontend created

kubectl -n demo get DestinationRule
# NAME          HOST          AGE
# sa-frontend   sa-frontend   3s


kubectl describe DestinationRule sa-frontend -n demo

# Удалить 
kubectl delete DestinationRule sa-frontend -n demo
kubectl -n demo delete deployment sa-frontend-green
```
###### Зеркалирование
```
Shadowing («экранирование») или Mirroring («зеркалирование») применяется в тех случаях, 
когда мы хотим протестировать изменение в production, 
не затронув конечных пользователей: для этого мы дублируем («зеркалируем») 
запросы на второй экземпляр, где произведены нужные изменения, и смотрим на последствия. 

```
```bash
# создадим второй экземпляр SA-Logic с багами 
kubectl apply -f ./K8S/istio/example_4/source/kube/shadowing/sa-logic-service-buggy.yaml -n demo

kubectl get pods -l app=sa-logic --show-labels -n demo
# NAME                              READY   STATUS    RESTARTS       AGE     LABELS
# sa-logic-7978b89489-jlv4c         2/2     Running   6 (153m ago)   8d      app=sa-logic,version=v1
# sa-logic-7978b89489-mfzbb         2/2     Running   6 (153m ago)   8d      app=sa-logic,version=v1
# sa-logic-buggy-77d79c9ddb-426wn   2/2     Running   0              2m44s   app=sa-logic,version=v2
# sa-logic-buggy-77d79c9ddb-4tj7f   2/2     Running   0              2m44s   app=sa-logic,,version=v2

# Сервис sa-logic нацелен на pod'ы с лейблом app=sa-logic, поэтому все запросы будут распределены между всеми экземплярами
# чтобы запросы направлялись на экземпляры с версией v1 и зеркалировались на экземпляры с версией v2
# Добьёмся этого через VirtualService в комбинации с DestinationRule, 
# где правила определят подмножества и маршруты VirtualService к конкретному подмножеству.

# ./K8S/istio/example_4/source/kube/ab-test/destinationrule-sa-frontend.yaml

```

```bash 
# Без зеркалирования скрипт нагрузочного тестирования показывает ошибки, после включения зеркалирования 
# ошибки уходят 

# {"timestamp":1770551150289,"status":500,"error":"Internal Server Error","exception":"org.springframework.web.client.HttpServerErrorException","message":"500 Internal Server Error","path":"/sentiment"}HTTP/1.1 500 Internal Server Error
# content-type: application/json;charset=UTF-8
# date: Sun, 08 Feb 2026 11:46:20 GMT
# x-envoy-upstream-service-time: 30046
# server: istio-envoy
# transfer-encoding: chunked
# 
# {"timestamp":1770551180454,"status":500,"error":"Internal Server Error","exception":"org.springframework.web.client.HttpServerErrorException","message":"500 Internal Server Error","path":"/sentiment"}HTTP/1.1 200 OK
# content-type: application/json;charset=UTF-8
# date: Sun, 08 Feb 2026 11:46:20 GMT
# x-envoy-upstream-service-time: 9
# server: istio-envoy
# transfer-encoding: chunked

```

```
```yaml 
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: sa-logic
spec:
  host: sa-logic    # определяет, что это правило применяется только к случаям, когда маршрут идёт в сторону сервиса sa-logic;
  subsets:
  - name: v1        # Названия (name) подмножеств используются при маршрутизации на экземпляры подмножества
    labels:
      version: v1   # Лейбл (label) определяет пары ключ-значение, которым должны соответствовать экземпляры, чтобы стать частью подмножества
  - name: v2
    labels:
      version: v2
```

```bash

kubectl apply -f ./K8S/istio/example_4/source/kube/ab-test/sa-logic-subsets-destinationrule.yaml -n demo

kubectl -n demo get DestinationRule
# NAME       HOST       AGE
# sa-logic   sa-logic   23s

kubectl apply -f ./K8S/istio/example_4/source/kube/ab-test/sa-logic-subsets-shadowing-vs.yaml -n demo
# cм pic_kiali_3.png


```
```bash
# Запустими нагрузку 
while true; do curl -v  http://192.168.1.171:8080/sentiment \
    -H "Content-type: application/json" \
    -d '{"sentence": "I love yogobella"}'; \
    sleep .8; done

```

```bash
# на мониторинге можно увидеть что багованя верся отдает нормально от 20 -40 % запросов 
# в отличии от нормальной версии 

```
###### Canary Deployments
```bash
# Canary Deployment — процесс выкатывания новой версии приложения для небольшого числа пользователей.
# сразу отправим 20 % пользователей на версию с багами (она и будет представлять наш канареечный выкат), 
# а оставшиеся 80 % — на нормальный сервис

# Обновим прошлую конфигурацию VirtualService для sa-logic следующей командой:

kubectl apply -f ./K8S/istio/example_4/source/kube/canary/sa-logic-subsets-canary-vs.yaml -n demo

# часть запросов приводит к сбоям
```
```bash 
while true; do \
   curl -i http://192.168.1.171:8080/sentiment \
   -H "Content-type: application/json" \
   -d '{"sentence": "I love yogobella"}' \
   --silent -w "Time: %{time_total}s \t Status: %{http_code}\n" \
   -o /dev/null; sleep .1; done

# Time: 0.111355s          Status: 500
# Time: 0.020223s          Status: 200

```
###### Таймауты и повторные попытки
```

# добавить таймаут, если сервис отвечает дольше 8 секунд,
# предпринимать повторную попытку, если у запроса происходит сбой.
# тк добавили повторные попытки - успешных ответов стало больше 
# cм pic_mon_3.png
```
kubectl apply -f ./K8S/istio/example_4/source/kube//time_out/sa-logic-retries-timeouts-vs.yaml -n demo


```bash 
# Удалить 
kubectl delete DestinationRule sa-logic -n demo
```









