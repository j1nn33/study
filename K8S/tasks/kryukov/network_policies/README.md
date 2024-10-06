## Network Policies

[Сетевые политики](https://kubernetes.io/docs/concepts/services-networking/network-policies/) - аналог сетевого firewall.
Позволяют ограничивать сетевой трафик на уровне IP адресов и портов.
[Network Policies API](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.27/#networkpolicy-v1-networking-k8s-io).

### Теория
### Тестовый стенд 
### Policy
#### - Ingress
#### - Deny All
#### - Разрешение подключения из namespace
#### - Две сетевых политики
#### - Два правила в одной политике
#### - Разрешение доступа на конкретный порт пода
#### - Egress

#### Теория
```
Объекты, которые можно использовать в сетевых политиках, определяются с помощью комбинации следующих 3-х идентификаторов:

podSelector       - поды.             (ограничение трафика с подов и на поды)
namespaceSelector - namespaces.       (ограничение трафика с одного namespace и на другие namespace)
ipBlock           - блоки IP адресов. (ограничение трафика с одних сетей в другие по IP)

При создании сетевой политики на основе пода или namespace используется labels для того, что бы определить
к каким или от каких подов или namespaces возможен трафик. Это похоже на использование selector у Service.

В kubernetes существует два типа изоляции пода: 
        Egress - исходящий сетевой трафик. 
        Ingress - входящий сетевой трафик.

- По умолчанию не установлено никаких ограничений. Т.е. любой трафик от пода и к поду разрешён.
- При включении Network Policies всегда будет разрешен локальный трафик пода (аналог localhost) и подключения,
  определённые в политике.
- Если определяется несколько сетевых политик - они объединяются. Сетевые политики не противоречат друг другу, а 
  дополняют друг друга. (возможно будут пробелмы при объединении)
- Чтобы разрешить подключение от исходного пода к целевому поду, необходимо разрешить подключение как в политике 
  Egress в исходном поде, так и в политике Ingress в целевой поде.
```
#### Тестовый стенд 
```
# Схема тестового стенда  ./K8S/tasks/kryukov/network_policies/image/test_stand.jpg
# манифесты размещены в ./K8S/tasks/kryukov/network_policies/test_stand/

# Создание 2-х namespace 
kubectl apply -f namespace.yaml
```
###### namespace app1
```
kubectl apply -f app1pod1.yaml

# Сам Ingress Classes был развернут по ./K8S/tasks/kryukov/network/ingress.md
# ingress controller (Over a NodePort Service)
kubectl apply -f ingressapp1pod1.yaml

http://192.168.1.171:30180/
https://192.168.1.171:30443/

# Тестирование см. ниже 
```
###### namespace app2
```
kubectl apply -f app2pod1.yaml
kubectl apply -f app2pod2.yaml
# Тестирование см. ниже 
```
###### namespace default
```
kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools
```
###### Тестирвание если что-то не так 
```
kubectl get all -o wide -n <name_namespace>
kubectl get all -o wide -n app1
# NAME                                        READY   STATUS    RESTARTS   AGE     IP             NODE                  NOMINATED NODE   READINESS GATES
# pod/app1-pod1-deployment-546cc875b9-k5zvt   1/1     Running   0          5m30s   10.233.66.24   control1.kube.local   <none>           <none>
# NAME                        TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE     SELECTOR
# service/service-app1-pod1   ClusterIP   10.233.11.150   <none>        81/TCP    5m30s   app=app1-pod1
# NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                           SELECTOR
# deployment.apps/app1-pod1-deployment   1/1     1            1           5m30s   app1-pod1    openresty/openresty:centos-rpm   app=app1-pod1
# NAME                                              DESIRED   CURRENT   READY   AGE     CONTAINERS   IMAGES                           SELECTOR
# replicaset.apps/app1-pod1-deployment-546cc875b9   1         1         1       5m30s   app1-pod1    openresty/openresty:centos-rpm   app=app1-pod1,pod-template-hash=546cc875b9

# из хоста и из пода из любого namespace
curl http://10.233.66.24:80
curl http://10.233.11.150:81
cat /usr/local/openresty/nginx/html/index.html

# из пода (в пределах совего namespace)
curl http://service-app1-pod1:81
curl http://app1-pod1-deployment-546cc875b9-k5zvt:80

# для обращения из другого namespace из pod к service 
#
# curl http://service-app2pod1.app2:81
# <h1>Тестовая страница app2pod1</h1>
# 
# curl http://service-app2pod2.app2:81
# <p>Простая тестовая страница app2pod2</a>.
```
#### POLICY
#### Ingress
```
# По умолчанию доступ к приложению открыт:

http://192.168.1.171:30180/
https://192.168.1.171:30443/

```
#### Deny All
```
В namespace app2 запретим весь входящий трафик.
Применяется только на namespace (глобальную сетевую политику сделать нельзя)

# FROM app1 default TO app2
#
curl http://service-app2-pod1.app2:81
curl http://service-app2-pod2.app2:81

# FROM app2 TO app2
#

curl http://service-app2-pod2.app2:81
curl http://service-app2-pod1:81

curl http://localhost:80


# FROM app2 TO app1 default
#
curl http://service-app1-pod1.app1:81

```
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: default-deny-all
  # определяет namespace, к подам которого будет применяться сетевая политика.
  namespace: app2
spec:
  policyTypes:
  # указываем типы политик которые используем их 2 шт Ingress/Egress отдельно или вместе 
  - Ingress
  # podSelector пуст. Это означает, что он будет соответствовать всем подам. Таким образом, политика будет применена ко всем подам в namespace app2
  # для pod по умолчанию трафик разрешен, но как только для pod будет указана политика (по умолчаню становиться deny all) и надо писать разрешающие правила
  # ingress пустой массив (нет разрешающих правил). Поскольку правила отбора трафика не указаны, по умолчанию запрещается весь трафик к подам, выбранным при помощи podSelector. 
  podSelector: {}
  ingress: []
```
```
kubectl apply -f np/np-01.yaml

# т.к. политики относятся к namespace его указываем 
kubectl -n app2 get networkpolicies

# NAME               POD-SELECTOR   AGE
# default-deny-all   <none>         62s

# Проверим, что выдаст приложение
# FROM app1 default TO app2
#
curl http://service-app2-pod1.app2:81
curl http://service-app2-pod2.app2:81

# После задержки, вызванной невозможностью из app1, default получить доступ к приложениям в namespace app2, поучим сообщение об ошибке:
# curl: (7) Failed to connect to service-app2-pod1.app2 port 81: Connection timed out

# FROM app2 TO app2
#
# из app2 pod1 - запрещено
curl http://service-app2-pod2.app2:81
curl http://service-app2-pod1:81
# curl: (7) Failed to connect to service-app2-pod1.app2 port 81: Connection timed out

curl http://localhost:80
# <h1>Тестовая страница app2-pod1</h1>

# FROM app2 TO app1 default
#
# Запросы исходящие - разрешены 
curl http://service-app1-pod1.app1:81
<h1>Тестовая страница app1-pod1</h1>

```
#### Разрешение подключения из namespace

```
# Начальное состояние см. выше + применненая политика np-01.yaml
# Если мы хотим оставить политику по умолчанию deny + разрешить доступ из определенного namespace (app1). Нам потребуется
# добавить еще одну сетевую политику в namespace app2.

# посмотреть labels
kubectl get all -o wide -n app2

```
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-from-ns-app1
  namespace: app2
spec:
  policyTypes:
  - Ingress
  podSelector:
    # podSelector при помощи matchLabels указываем поды для которых будет работать сетевые правила.
    matchLabels:
      app: app1-pod1
  # В ingress определяем правила для входящего трафика.
  ingress:
    # В массиве from определяются два условия Оба условия объединяются логическим AND.
    - from:
      - namespaceSelector:
          # из какого namespace разрешен трафик
          matchLabels:
            kubernetes.io/metadata.name: app1
        podSelector: 
          # из какого namespace разрешен трафик
          matchLabels:
            app: app1-pod1
            #app.kubernetes.io/instance: app1  второй вариант лейбы 
```
# Важное замечание по поводу AND и OR.
# Это AND:
```
```yaml
- from:
  - namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: app1
    podSelector: 
      matchLabels:
        app: app1
```
```
# Это OR:
```
```yaml
- from:
  - namespaceSelector:
      matchLabels:
        kubernetes.io/metadata.name: app1
  - podSelector: 
      matchLabels:
        app: app1
```
```
# Применим сетевую политику:

kubectl apply -f np/np-02.yaml

kubectl -n app2 get networkpolicies
# NAME                 POD-SELECTOR    AGE
# allow-from-ns-app1   app=app2-pod1   60m
# default-deny-all     <none>          29m

kubectl describe networkpolicy allow-from-ns-app1 -n app2
# Name:         allow-from-ns-app1
# Namespace:    app2
# Spec:
#   PodSelector:     app=app2-pod1
#   Allowing ingress traffic:
#     To Port: <any> (traffic allowed to all ports)
#     From:
#       NamespaceSelector: kubernetes.io/metadata.name=app1
#       PodSelector: app=app1-pod1
#   Not affecting egress traffic
#   Policy Types: Ingress



# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Operation timed out
curl http://service-app2-pod1.app2:81
# curl: (7) Failed to connect to service-app2-pod1.app2 port 81: Operation timed out

# Удалим политику `default-deny-all`:
kubectl delete -f np/np-01.yaml

# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>. 

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>.
curl http://service-app2-pod1.app2:81
# curl: (7) Failed to connect to service-app2-pod1.app2 port 81: Operation timed out

# Можно сделать вывод: Если к поду подключена какая-либо сетевая политика, доступ к нему становится по умолчанию:
# "всё запрещено, разрешено только то, что разрешено".

# Вернем обратно политику по умолчанию для namespace app2:
kubectl apply -f np/np-01.yaml
```

#### Две сетевых политики
```
# Добавим разрешение доступа к приложению app2 из namespace default:
kubectl apply -f np/np-03.yaml
```
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-from-ns-default
  namespace: app2
spec:
  policyTypes:
  - Ingress
  podSelector: {}
  ingress:
    - from:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: default
        podSelector: {}
```
```
# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Connection timed out

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>.
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.

```
```
# Удалим политику `allow-from-ns-app1`

kubectl delete -f np-02.yaml

# FROM app1 TO app2
curl http://service-app2-pod1.app2:81 --connect-timeout=3
curl: (28) Connection timed out after 3001 milliseconds
curl http://service-app2-pod2.app2:81 --connect-timeout=3
curl: (28) Connection timed out after 3001 milliseconds

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>.
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.

#В результате удаления политики приложение app1 из namespace app1 потеряло доступ к подам namespace app2. А приложение
# из namespace default доступ сохранило.

# Удалим политику `allow-from-ns-default`

kubectl delete -f np-03.yaml
```

#### Два правила в одной политике
```
# В принципе можно правила из политик `allow-from-ns-app1` np-02.yaml и `allow-from-ns-default` np-03.yaml описать в одной политике.
```
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-from-ns-app1-and-default
  namespace: app2
spec:
  policyTypes:
    - Ingress
  # Но тут придется пожертвовать podSelector. В этом варианте политика будет применяться ко всем подам в namespace app2.   
  podSelector: {}
  ingress:
    # В from указываем два правила. Поскольку это два элемента массива, они объединяются логическим OR.
    - from:
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: app1
          podSelector:           
            matchLabels:
              app: app1-pod1
        - namespaceSelector:
            matchLabels:
              kubernetes.io/metadata.name: default             
          podSelector: {}
```
```
# Убедимся, что в namespace app2 осталась только политика `default-deny-all`:

kubectl -n app2 get networkpolicies
# NAME               POD-SELECTOR   AGE
# default-deny-all   <none>         8m25s

# Добавим политику allow-from-ns-app1-and-default:
kubectl apply -f np/np-04.yaml

# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>.

# FROM default TO app2
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>.
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.

```
#### Разрешение доступа на конкретный порт пода
```
# Если необходимо открывать доступ к определённым портам пода, можно немного модифицировать предыдущую сетевую политику:
```
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-from-ns-app1-and-default
  namespace: app2
spec:
  policyTypes:
    - Ingress
  podSelector: {}
  ingress:
  # мы управляем портами пода, а не сервиса
  # В NetworkPolices мы не можем использовать сервисы для описания правил!
 
    - ports:
        - port: 80
          protocol: TCP
    - from:
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: app1
        podSelector:
          matchLabels:
            app.: app1-pod1
      - namespaceSelector:
          matchLabels:
            kubernetes.io/metadata.name: default
        podSelector: {}
```
```
# В политиках при помощи endPort можно указывать диапазон портов:
```
```yaml
    - ports:
        - protocol: TCP
          port: 30000
          endPort: 32000
```

#### Правила Egress
```
# В качестве примера в namespace app1 разрешим всем подам исходящий трафик только в namespace app2.
# В сетевой политике вместо matchLabels показан пример использования matchExpressions.
```
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-to-ns-app2
  namespace: app1
spec:
  # исходящий трафик из app1 для всех pod 
  policyTypes:
    - Egress
  podSelector: {}
  egress:
  - to:
    - namespaceSelector:
        matchExpressions:
        - key: kubernetes.io/metadata.name
          operator: In
          values:
            - app2
            - some_label 
```
```
# Применим сетевую политику:
kubectl apply -f np-05.yaml
# Удалим все сетевые политики из namespace app2. Если они там остались.
# Попробуем подключиться из приложения app1 к app2:

# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# curl: (6) Could not resolve host: service-app2-pod1.app2
curl http://service-app2-pod2.app2:81
# curl: (6) Could not resolve host: service-app2-pod2.app2

# Проблема в доступе к DNS серверу кубера. Определив политику для исходящего
# трафика мы закрыли исходящий трафик от пода к DNS.
# Добавим вторую политику, разрешающую доступ к DNS:
```
```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-to-kubedns
  namespace: app1
spec:
  policyTypes:
    - Egress
  podSelector: {}
  egress:
    - to:
      - ipBlock:
          cidr: 169.254.25.10/32
      ports:
        - port: 53
          protocol: UDP
        - port: 53
          protocol: TCP
```
```
# в  кластере кубера используется nodelocaldns, (см как разворачивали) приземлённый на IP адрес на каждой ноде кластера. 
# поэтому указываем явно IP адрес
# Пример другого способа определения доступа к DNS северу можно посмотреть в np-07.yaml.

# Применим сетевую политику:
kubectl apply -f np-06.yaml

# Попробуем подключиться из приложения app1 к app2:
# FROM app1 TO app2
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>.
```

