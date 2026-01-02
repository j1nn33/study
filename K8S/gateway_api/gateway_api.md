##### GATE WAY API

###### Актуализация знаний ingress
###### GATEWAY
###### Gateway vs Ingress
###### DOC
###### gateway.yaml
###### HTTPRoute
###### Othet




###### Актуализация знаний ingress

```
ingress 

есть манифест (file.yaml) 
должен быть controller (который этот манифест понимаме и что-то с ним может сделать) ingress controller

см рис ingress_v1.png

kind: ingress - манифест (описывается движение трафика на APP) ассоциируется с ingressClass
kind: ingress controller - контролеер (ngins, haproxy, envoy, traefic ...) который понимает что надо делать с манифестом 
kind: ingressClass - к которому привязывается ingress controller (ingress controller обслуживат ingressClass)

Механика 

при появлении\изменении ingress, который ассоциирован с ingressClass 
ingress controller который привязан к ingressClass (понимате через связь с ingressClass что это к нему)
читает ingress и производет маршрутизацию трафика через себя на APP
```

###### GATEWAY 
```
см рис gate_way_controller_v1.png

kind: Pod Gateway controller  - приложение которое раелизует рекацию на новые типы kind: GatewayClass (может быть много) 
kind: GatewayClass  такой же функционал как у ingressClass
kind: Gateway  - привязыватся GatewayClass  (указываем GatewayClass и какими портами (порт Pod Gateway controller) и протоколами будет пользоваться)
kind: Route (HTTPRoute, TLSRoute, GRPSRoute, TCP/UDPRoute) - привязыватся Gateway

```
###### Gateway vs Ingress

```
1 - ingress (только HTTP - трафик обрабатывает)
2 - Gateway - ролевая модель
3 - отличия только в конфигурации, с точки зрения сетевого взаимодействия различий нет

Ролевая модель
infra provider    - готовит Gateway controller (указывает какие порты слушает контролер )
cluster operator  - опиывает Gateway и привязывается к GatewayClass и определяте inbound - какие входные точни Gateway controller будут использованы и кто может его использовать (namespace kind)
developer         - описывает Route и пирвызывает его  Gateway
```

###### DOC
```
Документация.                  https://kubernetes.io/docs/concepts/services-networking/gateway/
Документация на сайте проекта. https://gateway-api.sigs.k8s.io/
Реализации контроллеров.       https://gateway-api.sigs.k8s.io/implementations/

VIDEO                          https://rutube.ru/video/d8cb40436f7bc82891e02cc55b935ed9/
git                            https://github.com/BigKAA/youtube/tree/master/gatewayapi

```
###### gateway.yaml

```yaml
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: traefik-gateway
  namespace: sample
spec:
  gatewayClassName: traefik
  # что значение port - это номер порта контейнера контроллера. Номера портов берем из настроек самого traefik.
  # Посмотреть какие entryPoints определены при запуске можно в манифесте пода.
  # --entryPoints.metrics.address=:9100/tcp
  # --entryPoints.traefik.address=:8080/tcp
  # --entryPoints.web.address=:8000/tcp
  # --entryPoints.websecure.address=:8443/tcp
  
  listeners:
    - name: web
      port: 8000
      protocol: HTTP
      allowedRoutes:
        namespaces:
          from: All
    - name: https
      protocol: HTTPS
      port: 8443
      # hostaname для HTTPS и TLS listeners обязательно!
      hostname: sample.www.local
      tls:
        mode: Terminate
        certificateRefs:
          - name: sample-tls
            namespace: sample
      allowedRoutes:
	  # указваются разрешение (с какого нейспейса разрешено )
        namespaces:
          from: All
		  
```
##### HTTPRoute
```
 Gateway и Service на которые мы ссылаемся, могут находиться в разных namespaces.
```
```yaml

apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: sample-http
  namespace: sample
spec:
  parentRefs:
  # ссылаемся на Gateway, которы планируем использовать.
    - name: traefik-gateway
	  # указание секции listnera в Gateway
      sectionName: web
      kind: Gateway
      # namespace: sample
  hostnames:
    - "sample.www.local"
  rules:
  # описываем непосредственно маршрут пересылки.
    - backendRefs:
	    # в какой Service и куда пересылаем
        - kind: Service
          name: whoami
          namespace: sample
          port: 80
      matches:
        - path:
            type: PathPrefix
            value: /


```
###### Other
```
Gateway - два https listener и cert-manager
TCPRoute  (проброс ssh)
https://rutube.ru/video/be0b625a402df6a2479b6c2fcfa73e0c/


```




