###### Выходной шлюз

```
ServiceEntry, DestinationRule, VirtualService и Gateway


Пример 

прокси на выходе istio-egressgateway.istio-system.svc.cluster.local 

внешний сайт получателя, до которого мы пытаемся добраться

Определение ServiceEntry, отображаемое в выходной шлюз
kind: ServiceEntry ./K8S/istio/source/se-egress-gw.yaml

Выходной шлюз настроен на прием исходящего трафика, адресованного wikipedia.org
kind: Gateway      ./K8S/istio/source/egress-gw-wiki.yaml


Нужно, чтобы выходной шлюз получал адрес wikipedia.org с помощью DNS
и пересылал запрос на этот адрес, а у нас все прокси в сетке настроены 
на пересылку запросов на имя wikipedia.org в выходной 
шлюз (поэтому прокси на выходе перешлет сообщение себе же или отбросит 
его). Чтобы исправить ситуацию, воспользуемся возможностью привязки Vir
tualService к Gateway и направим трафик для wikipedia.org на некоторое фиктивное имя, 
например egress-wikipedia-org
kind: VirtualService 
```
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: egress-wikipedia-org
spec:
  hosts:
  – wikipedia.org
  gateways:
  – https-wikipedia-org-egress
  tls:
  – match:
    – ports: 443
      sniHosts:
      – wikipedia.org
    route:
    – destination:
      host: egress-wikipedia-org

```

```
определим ServiceEntry для разрешения egress-wikipedia-org через DNS как wikipedia.org
kind: ServiceEntry
```
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: egress-https-wikipedia-org
spec:
  hosts:
  – egress-wikipedia-org
  ports:
  – number: 443
    name: https
    protocol: HTTPS
  location: MESH_EXTERNAL
  resolution: DNS
  endpoints:
  – address: wikipedia.org
    ports:
      http: 443

```
```
Теперь трафик будет пересылаться на внешний сайт с помощью выделенно
го выходного шлюза. По умолчанию Istio позволяет передавать трафик адре
сатам, не имеющим записей ServiceEntry. Однако для большей безопасности 
эту настройку по умолчанию следует отключить, а сервисы вне сетки внести 
в белый список, создав для них записи ServiceEntry. Чтобы разрешить доступ 
к внешнему сервису в обход выходного шлюза, достаточно создать для нее 
идентификатор ServiceEntry:

```
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: ServiceEntry
metadata:
  name: egress-https-wikipedia-org
spec:
  hosts:
  – wikipedia.org
  ports:
  – number: 443 
      name: https 
      protocol: HTTPS
  location: MESH_EXTERNAL 
  resolution: DNS 
  endpoints:
  – address: istio-egressgateway.istio-system.svc.cluster.local
    ports:
      http: 443
```