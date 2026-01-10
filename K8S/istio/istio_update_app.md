##### Canary \ blue-green strategy

```
Возможность маршрутизации трафика на основе метаданных запроса, таких как URI запроса, его заголовки, 
IP-адреса источника/назначения и других. Единственным ключевым ограничением является то, что Istio 
не будет выполнять маршрутизацию, основанную на содержимом запроса.

Маршрутизация в VirtualService с сопоставлением путей
```
```yaml

apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  Name: foo-bars-svc
spec:
  hosts:
  – bar.foo.svc.cluster.local
  http:
  – match:
  – uri:
      exact: "/assets/static/style.css"
  route:
  – destination:
      host: webserver.frontend.svc.cluster.local
  – match:
  – uri:
     # Совпадение запросов вида “/foo/132:myCustomMethod”
     regex: "/foo/\\d+:myCustomMethod"
  route:
  – destination:
      host: bar.foo.svc.cluster.local
      subset: v3
  – route:
  – destination:
      host: bar.foo.svc.cluster.local
      subset: v2

```
```
Перенаправление запросов на основе наличия значения в cookieфайле
```
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  Name: dev-webserver
spec:
  hosts:
  – webserver.company.com
  http:
  – match:
  – headers: 
      cookie:
        environment: "dev"
  route:
  – destination:
      host: webserver.dev.svc.cluster.local
  – route:
  – destination:
      host: webserver.prod.svc.cluster.local
```

##### blue-green
```
В методике сине-зеленого развертывания бок о бок устанавливаются две версии приложения, старая и новая, и пользовательский трафик переключается 
со старого набора на новый. Это позволяет быстро вернуться к предыдущей рабочей версии, если что-то пойдет не так, – нужно лишь переключить 
пользовательский трафик с нового набора на старый (в противоположность стратегии скользящего обновления, в которой для отката к предыдущей 
версии сначала нужно заново развернуть двоичный файл предыдущей версии).

Объявляются две подгруппы сервиса с помощью DestinationRule, а затем VirtualService 
используется для направления трафика к одной или другой подгруппе

Вместо использования меток "синий" и "зеленый" в DestinationRule используем номера версий
```
```
Определение подмножеств
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
  – name: v2
      labels:
        version: v2
```
```
VirtualService, направляющий весь трафик в кластере
```
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: foo-blue-green-virtual-service
spec:
  hosts:
  – foo.default.svc.cluster.local
  http:
  – route:
    – destination:
        host: foo.default.svc.cluster.local
        subset: v1
```
```
перейти к другому набору, достаточно обновить VirtualService, направив трафик в целевое подмножество v2
```
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: foo-blue-green-virtual-service
spec:
  hosts:
  – foo.default.svc.cluster.local
  http:
  – route:
    – destination:
        host: foo.default.svc.cluster.local
        subset: v2
```
```
Канареечные развертывания
Канареечное развертывание – это практика отправки небольшой части трафика 
в новые рабочие нагрузки и постепенное его увеличение, пока весь трафик не 
будет обслуживаться новыми рабочими нагрузками. Цель состоит в проверке 
работоспособности новой рабочей нагрузки (запущена, работает и не возвращает ошибок) перед отправкой ей всего трафика

простой способ – разделить трафик по процентам. Для начала можно отправить 5% трафика 
в новую версию и, постепенно продвигая новые конфигурации VirtualService, увеличить трафик в новую версию до 100%
./K8S/istio/source/canary-shift.yaml

использовать Istio для установки cookie trusted-tester
./K8S/istio/source/canary-cookie.yaml

```

