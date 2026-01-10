##### NET
```
Pilot

Pilot использует три основных источника конфигурации:
- Конфигурация сетки
  Набор глобальных конфигураций для сервисной сетки.
- Конфигурация сети
  Конфигурации ServiceEntrie, DestinationRule, VirtualService, Gateway и прокси.
- Механизм обнаружения сервисов (Kubernetes API Server, Consul и Eureka)
```

```
Конфигурация сетки – это статический набор глобальных конфигураций для ее установки. 

 распределена по трем объектам:
- MeshConfig (mesh.istio.io/v1alpha1.MeshConfig)
  описывает настройку взаимодействий между компонентами Istio, 
  местонахождение источников конфигурации и т. д.

- ProxyConfig (mesh.istio.io/v1alpha1.ProxyConfig)
  описывает параметры инициализации Envoy: местоположение начальной конфигурации, привязки портов и т. д

- MeshNetworks (mesh.istio.io/v1alpha1.MeshNetworks)
  описывает набор сетей, охватываемых сервисной сеткой, с адресами входных шлюзов каждой сети.

```

```
Сетевая конфигурация
- ServiceEntry определяет сервис по именам – как набор имен хостов, используемых клиентами для вызова сервиса.
- DestinationRule управляют взаимодействиями клиентов с сервисом, а именно: стратегии балансировки нагрузки, 
  обнаружения отклонений, обрыва цепи и организации пула используемых соединений; настройки TLS и т. д.
- VirtualService задают конфигурацию потока трафика к сервису: маршрутизация L7 и L4, формирование трафика, 
  повторные попытки, тайм-ауты и т. д. 
- Gateway Шлюзы определяют доступность сервисов из-за пределов сетки: какие имена хостов каким сервисам соответствуют, 
  как обслуживать сертификаты для этих хостов и многое другое. 
  Прокси управляют доступностью сервисов внутри сетки: какие сервисы доступны и каким клиентам.

```
```
istioctl proxy-config <bootstrap | listener | route | cluster> <kubernetes pod>
```
```
Gateway предоставляет физические приемники (привязанные к порту в сети), 
VirtualService (типа route)– виртуальные приемники (не привязанные к порту, но получающие трафик от физических приемников).

   ./K8S/istio/source/gw.yaml
   ./K8S/istio/source/vs.yaml
```

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: Gateway
metadata:
  name: foo-com-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
  - hosts:
    - "*.foo.com"
    port:
      number: 80
      name: http
      protocol: HTTP
```

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
 name: foo-default
spec:
 hosts:
 - bar.foo.com
 gateways:
 - foo-com-gateway
 http:
 - route:
   - destination:
       host: bar.foo.svc.cluster.local
```

 
``` 
# в сетевой конфигурации Istio принята модель адресации на основе имен (name-centric model), в которой:

Gateway         - экспортирует имена;
VirtualService  - определяет имена и маршруты к ним;
DestinationRule - описывает, как взаимодействовать с именованными приложениями;
ServiceEntry    - позволяет создавать новые имена.

см рис  ./K8S/istio/image/istio-traffik-tract.png

ServiceEntry – это способ ручного добавления/удаления сервисов в реестр (из 
реестра) Istio. К сервисам из реестра можно обращаться по именам и ссылаться 
на них в других конфигурациях Istio. В простейшем случае ServiceEntry можно 
использовать для связывания имен с IP-адресами
   ./K8S/istio/source/static-se.yaml
```
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: http-server
spec:
  hosts:
  - some.domain.com
  ports:
  - number: 80
    name: http
    protocol: http
  resolution: STATIC
  endpoints:
  - address: 2.2.2.2
```
На основе ServiceEntry прокси сетки будут направлять запросы на имя some.domain.com по IP-адресу 2.2.2.2. 
ServiceEntry можно использовать для преобразования имен, используемых в Istio, в имена, разрешаемые через DNS

 Istio не заполняет DNS-записи на основе ServiceEntry

    ./K8S/istio/source/dns-se.yaml
заставит прокси пересылать запросы к foo.bar.com на имя baz.com, используя DNS для его разрешения.
В данном примере заявлено, что сервис находится вне сетки (location: MESH_EXTERNAL), поэтому прокси не будут пытаться использовать mTLS.
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: external-svc-dns
spec:
  hosts:
  - foo.bar.com
  location: MESH_EXTERNAL
  ports:
  - number: 443
    name: https
    protocol: HTTP
  resolution: DNS
  endpoints:
  - address: baz.com
```

DestinationRule
позволяют описать, как клиент в сетке должен вызывать сервис, включая:
- подмножества сервисов (например, v1 и v2);
- стратегию балансировки нагрузки, которую должен использовать клиент;
- условия признания конечных точек сервиса неисправными;
- настройки пула соединений L4 и L7;
- TLS-настройки сервера.

Настройки пула соединений

разрешающее максимум четыре TCP-соединения на конечную точку назначения 
и максимум 1000 одновременных запросов HTTP2 через эти четыре TCP соединения.

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: foo-default
spec:
  host: foo.default.svc.cluster.local
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 4
      http:
        http2MaxRequests: 1000
```
```
 Настройки TLS
DISABLED     Отключает TLS для TCP-соединения.
SIMPLE       Инициирует TLS-соединение с конечной точкой назначения.
MUTUAL       Устанавливает mTLS-соединение с конечной точкой назначения.
ISTIO_MUTUAL Запрашивает, использует ли mTLS сертификаты, предоставлямые сеткой Istio.

DestinationRule для подключения к веб-сайту HTTPS за пределами сетки
( Разрешение покидать сетку исходящему трафику в домен http://google.com )
   ./K8S/istio/source/egress-destrule.yaml

DestinationRule, предписывающее использование mTLS
```

```yaml
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: remote-a-ingress
spec:
  host: ingress.a.remote.cluster
  trafficPolicy:
    tls:
      mode: MUTUAL
      clientCertificate: /etc/certs/remote-cluster-a.pem 
      privateKey: /etc/certs/client_private_key_cluster_a.pem 
      caCertificates: /etc/certs/rootcacerts.pem
```
```
Подмножества
позволяет разделить один сервис на подмножества с помощью меток.
Также можно для каждого подмножества отдельно конфигурировать все описанные выше функции,
которые позволяют настраивать DestinationRule. 
Например, можно разделить сервис на два подмножества на основе версии и использовать 
VirtualService для канареечного развертывания новой версии, 
постепенно переводя весь трафик на новую версию ( Каждая версия сервиса foo имеет 
свою собственную четко определенную политику балансировки нагрузки.)
```
```yaml

apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: foo-default
spec:
  host: foo.default.svc.cluster.local
  subsets:
  – name: v1
    labels:
      version: v1
    trafficPolicy:
      loadBalancer:
        simple: ROUND_ROBIN
   – name: v2
    labels:
      version: v2
    trafficPolicy:
      loadBalancer:
        simple: LEAST_CONN
```

##### Gateway
```
сконфигурирован для преобразования входящих HTTP/80 соединений в защищенные соединения HTTPS/443

   ./K8S/istio/source/gw-https-upgrade.yaml

Gateway настраивает поведение L4, а не L7   (порты и протоколы)
```
##### VirtualService
```
VirtualService описывает направление именованного трафика нескольким получателям 
Описывает L7


VirtualService привязывается к Gateway, если :
   - VirtualService включает имя Gateway в своем поле gateways;
   - по крайней мере один хост, заявленный VirtualService, экспортируется объектом Gateway.

Привязка VirtualService foo.com к Gatewa
   ./K8S/istio/source/foo-vs.yaml
   ./K8S/istio/source/gw-to-vses.yaml
```
#####  
