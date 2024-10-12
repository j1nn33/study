## Calico Network Polices

[Документация](https://docs.tigera.io/calico/latest/network-policy/).

### Особенности сетевых политик calico
### calicoctl
### Тестовый стенд
### Deny All
### Разрешение подключения из namespace
### GlobalNetworkPolicy  
```        
    - ./K8S/tasks/kryukov/calico_network_polices/GlobalNetworkPolicy.md    
    - Deny All  
    - Dev окружение
```
### Host Endpoint 
```
     - ./K8S/tasks/kryukov/calico_network_polices/network_polices/Host_Endpoint.md
     - Failsafe rules
     - apiVersion
     - Определение HostEndpoint
     - Firewall
     - ТЗ
     - Разрешить весь входящий и исходящий трафик
     - Вариант 1
     - Вариант 2
     - Разрешить трафик на loopback interface хостов кластера
     - Кластерные IP адреса.
     - Разрешить входящий трафик только на определённые сервисы типа NodePort
```
### Особенности сетевых политик calico
```
Политики могут быть применены к следующему типу конечных точек (endpoints): 
    - под
    - контейнер
    - виртуальная машина
    - сетевой интерфейс хоста.
Политики могут определять правила, которые применяются к:
    - Ingress
    - Egress
    - или обеим одновременно.
Поддерживается приоритет политик.
Правила политик поддерживают:
    - Действия: allow, deny, log, pass
    - Критерии отбора source и destination:
    - Порт: номер порта, диапазон портов, kubernetes имена портов.
    - Протоколы: TCP, UDP, ICMP, SCTP, UDPlite, ICMPv6, протокол по его номеру (1-255).
    - Атрибуты HTTP (при использовании Istio).
    - Атрибуты ICMP.
    - Версию IP - 4 или 6.
    - IP или CIDR.
    - Endpoint selectors (на базе kubernetes labels).
    - Namespace selectors.
    - Service account selectors.
Дополнительные элементы управления обработкой пакетов:
    - отключение connection tracking, 
    - применение перед DNAT,
    - применение к переадресованному трафику (forwarded traffic) и/или локально завершенному трафику (locally terminated traffic).
```
### calicoctl
```
# Для управления сетевыми политиками calico рекомендуется использовать утилиту calicoctl.
# Смотрите какая версия calico установлена в вашем кластере и скачиваете calicoctl соответствующей версии:
https://github.com/projectcalico/calico/releases/

# Посмотреть версию calico
# берем любой pod из namespace calico-system и смотрим версию image 
# calico-kube-controllers    Image: docker.io/calico/kube-controllers:v3.26.4

curl -Os -L https://github.com/projectcalico/calico/releases/download/v3.26.4/calicoctl-linux-amd64
mv calicoctl-linux-amd64 calicoctl
chmod +x calicoctl
sudo mv -f calicoctl /usr/local/bin
calicoctl version

# Почти со всеми объектами calico можно работать при помощи kubectl. Правда не так удобно как с calicoctl. 
# Для этого в системе должен быт установлен calico APIServer. Если calico был установлен при помощи оператора,
# APIServer включается автоматически.

kubectl get tigerastatus apiserver
# AVAILABLE = True
# NAME        AVAILABLE   PROGRESSING   DEGRADED   SINCE
# apiserver   True        False         False      113d

# Если оператор не включен (AVAILABLE = False), достаточно добавить его в систему при помощи следующего манифеста:
```
```yaml
apiVersion: operator.tigera.io/v1
kind: APIServer
metadata:
  name: default
spec: {}
```
```
# calicoctl по-прежнему требуется для следующих подкоманд:
# 
#  - calicoctl node
#  - calicoctl ipam
#  - calicoctl convert
#  - calicoctl version

calicoctl get ippool
# NAME                  CIDR             SELECTOR
# default-ipv4-ippool   10.233.64.0/18   all()

kubectl get ippool
# NAME                  CREATED AT
# default-ipv4-ippool   2024-06-16T15:43:25Z



```
### Тестовый стенд
```
# Тестовый стенд достался от предыдущего видео.
# ./K8S/tasks/kryukov/network_policies/README.md
# Для начала попробуем создать сетевые политики из предыдущего видео при помощи политик calico.
```
### Deny All
```
# В namespace app2 запретим весь входящий трафик.
```
```yaml
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: app2
spec:
  selector: all()
  types:
    - Ingress
```

```
calicoctl apply -f np-01.yaml

calicoctl get networkPolicy -n app2
# NAMESPACE   NAME
# app2        default-deny

# или в WEB Custom Resource Definitions/networkpolicies/ 

kubectl get networkPolicy.projectcalico.org -n app2
# NAME           CREATED AT
# default-deny   2024-10-07T18:27:48Z


# Проверяем работу приложений.
# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out.
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out
curl http://service-app2-pod1.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out
```
### Разрешение подключения из namespace

```yaml
kind: NetworkPolicy
apiVersion: projectcalico.org/v3
metadata:
  name: allow-from-ns-app1
  namespace: app2
spec:
  types:
    - Ingress
  selector: 'app == "app2-pod1"'
  ingress:
    - action: Allow
      protocol: TCP
      destination: {} # Не обязательно. Это значение по умолчанию.
      # from namespace:app1 pod: app1-pod1
      source:
        namespaceSelector: 'kubernetes.io/metadata.name == "app1"'
        # поды с app1-pod1
        selector: 'app == "app1-pod1"'
```

[Синтаксис выражений, используемых в `selector`](https://docs.tigera.io/calico/latest/reference/resources/networkpolicy#selectors)


```
calicoctl apply -f np-02.yaml
# Проверяем доступы:

# Проверяем работу приложений.
# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out
curl http://service-app2-pod1.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out

# Удалим политику Deny для namespace app2.
calicoctl delete -f np-01.yaml

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod2</a>.

# По аналогии со стандартными сетевыми политиками kubernetes: Если к поду подключена какая-либо сетевая политика, доступ к
# нему становится по умолчанию: "всё запрещено, разрешено только то, что разрешено".
```