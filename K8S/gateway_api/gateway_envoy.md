##### Envoy Gateway
##### Установка

##### Envoy Gateway
```
doc
https://gateway.envoyproxy.io/docs/

см рис gate_way_envoy_v1.png

kind: Pod Envoy Gateway Controller    - смотрит наличие манифестов (в зависимости от манифестов запускает отдельные kind: Pod Envoy Proxy)
                                        смотрит на kind: Service Endpoint (получает от туда ip подов и перенаправляте трафик напрямую в поды - по умолчанию)
                                        можно настроить и перенаправление трафика на kind: Service Endpoint
kind: EnvoyProxy                      - динамическая конфигурация  Envoy Proxy серверов
                                        в зависимости от того куда он привязан
                                            - к kind: GatewayClass то распространятся на kind: Pod Envoy Proxy (глобальный конфиг)
                                              т.е. она будет распространяться на все экземпляры envoy proxy, относящиеся к этому классу.
                                            - к kind: GateWay то к конкретному kind: Pod Envoy Proxy (локальный конфиг)                                        
kind: Pod Envoy Proxy                 - запускается на каждый kind: Gateway и создается отдельный kind: service NodePort | LoadBalancer
kind: ServiceEndpoint
kind: service NodePort | LoadBalancer - по умолчанию создается LoadBalancer (поэтому должно быть реализован механизм вывода его во вне (metalLB) )
```

##### Установка
```
# Metallb

./K8S/gateway_api/source/mlb.yaml
kubectl apply -f mlb.yaml

# Helm chart

https://hub.docker.com/r/envoyproxy/gateway-helm/tags

# ставим приложение по умолчанию:
helm install eg oci://docker.io/envoyproxy/gateway-helm --version v1.3.1 -n envoy-gateway-system --create-namespace

# Тестовое приложение

kubectl create ns sample
kubectl apply -f test-application.yaml


# Proxy Configuration
#Для каждого Gateway будет создаваться отдельный экземпляр прокси envoy. Конфигурация прокси происходит при помощи kind: EnvoyProxy. 
# Это особенность непосредственно envoy и никакого отношения к GatewayAPI не имеет.
# Конфигурацию можно привязать к GatewayClass. Тогда она будет распространяться на все экземпляры envoy proxy, относящиеся к этому классу. 
# Либо делать отдельную конфигурацию для каждого экземпляра Gateway. Т.е. для отдельного экземпляра envoy.

API EnvoyProxy. https://gateway.envoyproxy.io/docs/api/extension_types/#envoyproxy

```
```yaml

apiVersion: gateway.envoyproxy.io/v1alpha1
kind: EnvoyProxy
metadata:
  name: my-proxy-config
  namespace: sample
spec:
  logging:
    level: 
      # изменить информацию, выдаваемую envoy в логи для каждого компонента default, upstream
      default: warn
      upstream: info
  provider:
    type: Kubernetes
    kubernetes:
      envoyService:
        # externalTrafficPolicy у создаваемых сервисов с Local на Cluster
        externalTrafficPolicy: Cluster
        # можно указать nodeport
        type: LoadBalancer

```
```
kubectl apply -f EnvoyProxy-Config.yaml

```
GatewayClass
В GatewayClass подключаем конфигурацию EnvoyProxy
Имя контроллера gateway.envoyproxy.io/gatewayclass-controller задается по умолчанию при установке приложения. Но его можно изменить в файле values.yaml чарта
kubectl apply -f gateway-class.yaml

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: GatewayClass
metadata:
  name: eg
spec:
  controllerName: gateway.envoyproxy.io/gatewayclass-controller
  parametersRef:
    # Подключение конфигурации созданой выше EnvoyProxy-Config.yaml 
    group: gateway.envoyproxy.io
    kind: EnvoyProxy
    name: my-proxy-config
    namespace: sample
```

```
Создаем Gateway 

При создании Gateway добавим два liteners: http и https. 
Для работы последнего потребуются SSL сертификаты. Можно заранее создать сикрет с ними. 
Можно пользоваться cert-manager, который будет автоматически создавать и поддерживать работу с сертификатами.
(тут косяк смотри видео) создать серт нужно руками, а не анотацией в gateway

Важно понимать, что для работы cert-manager с GatewayAPI в кластере должны быть установлены CRD GatewayAPI!
Поэтому установка cert-manager будет производиться строго после envoyproxy gateway, в состав которого эти CRD входят.

helm -n cert-manager install cert-manager jetstack/cert-manager \
  --set="extraArgs[0]=--enable-gateway-api" \
  --set="crds.enabled=true" \
  --create-namespace


добавим Issuer

kubectl apply -f certs.yaml
```

```yaml
---
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: eg
  namespace: sample
  # annotations:
  #   cert-manager.io/cluster-issuer: dev-ca-issuer
  #   cert-manager.io/common-name: sample.web.local
  #   cert-manager.io/subject-organizations: "home dev lab"
  #   cert-manager.io/subject-countries: "RU"
  #   cert-manager.io/subject-localities: "Moscow"
  #   cert-manager.io/duration: "9125h"
  #   cert-manager.io/renew-before: "360h"
  #   cert-manager.io/usages: "server auth"
  #   cert-manager.io/private-key-algorithm: RSA
  #   cert-manager.io/private-key-encoding: "PKCS8"
  #   cert-manager.io/private-key-size: "4096"
  #   cert-manager.io/private-key-rotation-policy: Always
spec:
  gatewayClassName: eg
  listeners:
    # 2 listeners
    - name: http
      protocol: HTTP
      port: 80
      allowedRoutes:
        namespaces:
          from: All
    - name: https
      protocol: HTTPS
      port: 443
      # Косяк с серт менеджером см Видео
      # hostname: sample.web.local
      tls:
        mode: Terminate
        certificateRefs:
          - name: sample-tls
            namespace: sample
      allowedRoutes:
        namespaces:
          from: All

```
```

# Добавляем Gateway:

kubectl apply -f gateway.yaml

# Убеждаемся, что появился сервис типа LoadBalancer и под envoy proxy:

kubectl -n envoy-gateway-system get

# HTTPRoute
# Добавляем два HTTPRoute, по одному для каждого listener:

kubectl apply -f http-route.yaml
kubectl apply -f https-route.yaml

# Проверяем доступность нашего приложения через кластерный IP:

curl -H "Host: sample.web.local" http://192.168.1.180
curl -kH "Host: sample.web.local" https://192.168.1.180