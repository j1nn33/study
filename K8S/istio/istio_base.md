#### istio 

Istio — это сервисная сеть

```
- Безопасная связь между сервисами в кластере с взаимным TLS-шифрованием, надёжной аутентификацией и авторизацией на основе идентификационных данных.
- Автоматическая балансировка нагрузки для трафика HTTP, gRPC, WebSocket и TCP.
- Точное управление поведением трафика с помощью расширенных правил маршрутизации, повторных попыток, аварийного переключения и имитации сбоев.
- Подключаемый уровень политик и API конфигурации, поддерживающие контроль доступа, ограничения скорости и квоты.
- Автоматические показатели, журналы и трассировки для всего трафика внутри кластера, включая входящий и исходящий трафик кластера.

```
###### два режима работы istio:

Sidecar - когда в под приложения добавляются один (входящий трафик) или два (плюс исходящий трафик) контейнера с прокси серверами Envoy.
Ambient - устанавливается один прокси сервер на каждую ноду кластера для проксирования трафика на 4-м уровне (не envoy). И иногда дополнительные прокси сервера для работы на 7-м уровне для определенных namespaces (envoy).
Envoy - прокси для обработки входящего и исходящего трафиков для всех сервисов в сетке.

   Как это работает
Istio разделяет свои функции на два отдельных уровня. 
На базовом уровне ztunnel (отдельный proxy L4 mTLS - задача шифровать трафик) обеспечивает безопасную маршрутизацию и защиту трафика с нулевым доверием. 
При необходимости пользователи могут включить прокси-серверы L7 для доступа ко всему набору функций Istio. 
Прокси-серверы L7, хотя и более ресурсоёмкие, чем только ztunnel, по-прежнему работают как фоновый компонент инфраструктуры, не требуя внесения изменений в код приложений пользователей.

###### Архитектура и компоненты Istio   
./K8S/istio/image/istio_arch_1.png

```
Istio как service mech состоит из Data plane, Control plane
  - Data plane    (уровень данных) - набор прокси сервисов, sidecar в каждом pod (используется Envoy)
  - Control plane (уровень управления) управляет и настраивает sidecar, управляет метриками, TLS
```

```
Control plane Уровень управления Istio:
 - предоставляет политику и  конфигурацию сервисам в  сетке через API
   и позволяет администраторам задать требуемое поведение маршрутизации/отказоустойчивости;
 - объединяет набор изолированных прокси в сервисную сетку и предоставляет уровню данных:
    – API для передачи локализованной конфигурации;
    – абстракцию обнаружения сервисов;
 - использует API для определения политик через назначение квот и ограничений;
 - обеспечивает безопасность посредством выдачи и  ротации сертификатов;
 - назначает идентификатор рабочей нагрузке;
 - обрабатывает конфигурацию маршрутизации:
    – не анализирует никакие пакеты/запросы в системе;
    – определяет границы сетей и способы доступа к ним;
    – унифицирует сбор телеметрических данных.
```
```
Control plane состоит 
Pilot – (config proxy)наблюдает за состоянием и  местоположением запущенных сервисов и  предоставляет эту
        информацию уровню данных. Pilot взаимодействует с системой обнаружения сервисов и  отвечает за настройку прокси (компонент уровня данных istioproxy).
Galley - является компонентом агрегации и распределения конфигурации Istio. Galley использует протокол настройки сетки (Mesh Configuration Protocol, MCP) 
        в качестве механизма обслуживания и распределения конфигураций.
Mixer - отвечает за предварительную проверку условий, управление квотами, передачу телеметрии, политики 
        ./K8S/istio/image/istio_mixer_1.png
Citadel - mTLS PKI
```

###### Маршрутизация трафика 
Gateway  https://istio.io/latest/docs/reference/config/networking/gateway/

```
Входной шлюз  - обработка входящего в сетку трафика – это задача обратного проксирования, похожая на традиционную балансировку нагрузки веб-сервера.
Выходной шлюз - трафик может выходить из сервисной сетки Istio двумя путями: непосредственно из вспомогательных прокси или через выходной шлюз, в котором 
                можно применить дополнительные политики для управления исходящим трафиком
                Если требуется, чтобы исходящий трафик миновал выходной шлюз, это можно 
                сделать настройкой istio-sidecar-injector в ConfigMap. 
                Добавьте в конфигурацию следующий параметр, идентифицирующий локальные сети кластера 
                и удерживающий локальный трафик в пределах сетки, пересылая трафик для 
                всех остальных адресатов во внешнюю сеть:--set global.proxy.includeIPRanges="10.0.0.1/24"
```
```

CLIENT   ---> ROUTE ---> Ingress GATEWAY service ---> istio ingress Gateway pod ---> APP Service ---> APP POD
                         Egress  GATEWAY                 |               |
                                                         |               |
                                                      GATEWAY       VirtualService


```
```
GATEWAY        - описывате хосты и потры, listner L4
VirtualService - описывает маршрутизацию тарфика и отправляте его на service L7

               GATEWAY и VirtualService - управляют конфигурацие Envoy (Ingress Gateway controller)
               Ingress Gateway - состоит из envoy pod и k8s ingress

ROUTE          - привязывается к service и необходим для вызова сервиса снаружи кластера url        
```
```
######  Прохождение пакета 
1 пакет попадает на Loadbalancer который отправялет его на порт k8s workernode
2 на k8s workernode пакет попадает к Ingress GATEWAY service 
3 перенаправляется istio ingress Gateway pod
4  istio ingress Gateway pod настраивается через GATEWAY и VirtualService
         GATEWAY        порыт, протоколы, ssl - сертификаты
         VirtualService роутинг пакета к APP Service
5  istio ingress Gateway pod отправляет пакет на APP Service
6  APP Service отправляте на APP POD
```

```yaml
# конфигурация шлюза настраивает прокси для выполнения функций балансировки нагрузки
# и открывает доступ к портам 80 и 9080 (HTTP), 443 (HTTPS) и 2379 (TCP)
# Настройки шлюза будут применены к прокси, запущенному в поде с меткой app: my-gateway-controller
# необходимо убидться что внешний трафик в эти понрты разрешен в сети
apiVersion: networking.istio.io/v1
kind: Gateway
metadata:
  name: my-gateway
  namespace: some-config-namespace
spec:
  selector:
    app: my-gateway-controller
  servers:
  - port:
      number: 80
      name: http
      protocol: HTTP
    hosts:
    - us.bookinfo.com
    - eu.bookinfo.com
    tls:
      httpsRedirect: true  # отправляет ответ 301 для переадресации HTTP-запросов
  - port:
      number: 443
      name: https-443
      protocol: HTTPS
    hosts:
    - us.bookinfo.com
    - eu.bookinfo.com
    tls:
      mode: SIMPLE        # разрешает передачу HTTPS-трафика в этот порт
      serverCertificate: /etc/certs/servercert.pem
      privateKey: /etc/certs/privatekey.pem
  - port:
      number: 9443
      name: https-9443
      protocol: HTTPS
    hosts:
    - "bookinfo-namespace/*.bookinfo.com"
    tls:
      mode: SIMPLE # enables HTTPS on this port
      credentialName: bookinfo-secret # fetches certs from Kubernetes secret
  - port:
      number: 9080
      name: http-wildcard
      protocol: HTTP
    hosts:
    - "*"
  - port:
      number: 2379  # открывает доступ к сервису через порт 2379
      name: mongo
      protocol: MONGO
    hosts:
    - "*"



```


##### деинсталляция Istio
```
kubectl delete -f samples/addons
istioctl uninstall -y --purge
kubectl delete namespace istio-system
kubectl label namespace default istio-injection-

### If you ran any tasks that required the experimental version of the CRDs:

kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd/experimental?ref=v1.4.0" | kubectl delete -f -

### Otherwise:

kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.4.0" | kubectl delete -f -


kubectl get crds
kubectl get pods

```

##### установка с помощью Helm

```
kubectl create namespace istio-system
helm template install/kubernetes/helm/istio-init --name istio-init --namespace istio-system | kubectl apply -f 
helm template install/kubernetes/helm/istio --name istio --namespace istio-system | kubectl apply -f 

# докинуть параметры при установки
helm install install/kubernetes/helm/istio --name istio --namespace istio-system \
     --set global.controlPlaneSecurityEnabled=true \
	 --set mixer.adapters.useAdapterCRDs=false \
	 --set grafana.enabled=true --set grafana.security.enabled=true \
	 --set tracing.enabled=true \
	 --set kiali.enabled=true
	 
	 
# Проверка сетки после установки

kubectl get svc -n istio-system
kubectl get pods -n istio-system


# Деинсталляция с помощью Helm

helm template install/kubernetes/helm/istio --name istio --namespace istio-system | kubectl delete -f -
kubectl delete -f install/kubernetes/helm/istio-init/files
kubectl delete namespace istio-system

```





