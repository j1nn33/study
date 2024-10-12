### GlobalNetworkPolicy  
### Deny All  
### Разрешаем входящий трафик
### Dev окружение

Одна из фишек сетевых политик calico - это наличие глобальных политик, правила которых распространяются на весь кластер
kubernetes: kind: GlobalNetworkPolicy.

### Deny All

```
В качестве примера глобальной сетевой политики рассмотрим политику DenyAll. Запретим по умолчанию весь трафик.
Под правила запрета не должны попадать системные приложения кластера. Обычно это приложения, находящиеся в
namespace kube-system. Доступ приложений к DNS серверу кластера. Из под удара должны быть выведены другие системные 
приложения, участвующие, например в сборе метрик, организации сетевого трафика и т.п.

Посмотрим список namespaces, которые есть в  кластере:

kubectl get ns

# NAME                   STATUS   AGE
# app1                   Active   15d
# app2                   Active   15d
# calico-apiserver       Active   113d
# calico-system          Active   113d
# default                Active   113d
# ingress-nginx          Active   50d
# kube-node-lease        Active   113d
# kube-public            Active   113d
# kube-system            Active   113d
# kubernetes-dashboard   Active   83d
# metallb-system         Active   29d
# nfs-client             Active   82d
# tigera-operator        Active   113d
# volumes-sample         Active   98d


Подавляющее большинство из представленных namespaces содержат в себе либо системные, либо вспомогательные приложения.
Ограничение трафика на которые повлечет за собой написание большого количества сетевых политик.
Большое количество сетевых политик влечет за собой следующие риски:

- 1. Логические ошибки в правилах. Что-то забыли, где-то указали не тот порт.
- 2. Сложность отладки политик.
- 3. Снижение скорости сети. Чем больше правил, тем больше задержка на пути прохождения сетевого пакета.


Можно ограничиться разумным минимумом:

1. При помощи правил RBAC разрешить пользователям работать только в namespaces, где располагаются их приложения: app1 и
app2.
2. Создать глобальную политику DenyAll, затрагивающую только эти namespaces.

Заниматься перечислением в сетевой политике labels всех интересующих нас namespaces (имеется в виду перечисление по
именам) дело не благодарное. Списки могут быть слишком большие. Поэтому в качестве обязательного правила
администрирования кластера kubernetes следует сказать, что: "все пользовательские namespaces должны быть отмечены
labels policy: user". 

kubectl label namespace app1 policy=user
kubectl label namespace app2 policy=user
kubectl label namespace default policy=user


Напишем глобальную сетевую политику, которая будет работать только в трех namespaces, помеченных соответствующей меткой.

Политика должна содержать следующие правила:
-  Запретить по умолчанию весь входящий и исходящий трафик.
-  Разрешить исходящий трафик:
    - К nodelocaldns (это особенность кластера развернутого по ./K8S/ansible/kubeadm ).
    - К сервису kubernetes в namespace default (это сервис к которому обращаются приложения когда им необходимо обратиться к kubernetes API ).
```
```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: deny-policy-user
spec:
  namespaceSelector: 'policy == "user"'
  types:
  - Ingress        # тк внизу ее не описали, то политика по умолчанию DENY
  - Egress
  egress:          # разрешить исходящие соединения к nodelocaldns
  - action: Allow
    protocol: UDP
    destination:
      nets:
        - 169.254.25.10/32
      ports:
      - 53
  - action: Allow
    protocol: TCP
    destination:
      nets:
        - 169.254.25.10/32
      ports:
        - 53
  - action: Allow  # разрешить доступ к сервису kubernetes API в namespace default
    destination:
      services:
        name: kubernetes
        namespace: default
```

```
calicoctl apply -f np-03.yaml

# Посмотреть в WEB Custom Resource Definitions/globalnetworkpolicies

kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools

Проверим возможность подключения к приложениям и сервисам.
# FROM default TO app1, app2

curl http://service-app1-pod1.app1:81 --connect-timeout 5
# curl: (7) Failed to connect to service-app1-pod1.app1 port 81: Operation timed out
curl http://service-app2-pod1.app2:81 --connect-timeout 5
# curl: (7) Failed to connect to service-app2-pod1.app2 port 81: Operation timed out
curl http://service-app2-pod2.app2:81 --connect-timeout 5
# curl: (7) Failed to connect to service-app2-pod2.app2 port 81: Operation timed out

# FROM app1 kubernetes API in namespace default (запросы проходят)
curl -vk https://kubernetes.default.svc:443 
#  "kind": "Status",
#  "status": "Failure",
#  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
#  "reason": "Forbidden",

# FROM app2 kubernetes API in namespace default
curl -vk https://kubernetes.default.svc:443 
#  "kind": "Status",
#  "status": "Failure",
#  "message": "forbidden: User \"system:anonymous\" cannot get path \"/\"",
#  "reason": "Forbidden",
```
###  Разрешаем входящий трафик
```
Разрешим доступы к приложениям. Предполагается, что доступным должно быть только приложение app1.

Проверим:
http://192.168.1.171:30180/ 
# 504 Gateway Time-out
```

```yaml
---
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-to-app1
  namespace: app1
spec:
  types:
    - Ingress # разрешает входящий тафик для всех подов у котрых label app = app1-pod1
  selector: 'app == "app1-pod1"'
  ingress:
    - action: Allow
---
kind: NetworkPolicy  # исходяций трафик из пода в app2
apiVersion: projectcalico.org/v3
metadata:
  name: allow-to-ns-app2
  namespace: app1
spec:
  types:
    - Egress
  selector: 'app == "app1-pod1"'
  egress:
    - action: Allow
      destination:
        namespaceSelector: 'kubernetes.io/metadata.name == "app2"'
```
```
calicoctl apply -f np/np-04.yaml

# Посмотреть в WEB Custom Resource Definitions/networkpolicies.crd.projectcalico.org

# Проверяем:
http://192.168.1.171:30180/ 
Тестовая страница app1-pod1

# FROM app1 TO app2  (не разрешено тк нет разрешающей политики для app2 - будет ниже )
#
curl http://service-app2-pod1.app2:81
#  url: (7) Failed to connect to service-app1-pod1.app1 port 81: Operation timed out
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app1-pod1.app1 port 81: Operation timed out

№ Добавим политику Ingress в namespaces app2 для подов приложения app1 :
```
```yaml
kind: NetworkPolicy
apiVersion: projectcalico.org/v3
metadata:
  name: allow-to-nginx
  namespace: app2
spec:
  types:
    - Ingress   # доступ к приложению с label app2-pod1
  selector: app == 'app2-pod1'
  ingress:
    - action: Allow
      protocol: TCP
      source:
        namespaceSelector: 'kubernetes.io/metadata.name == "app1"'
```
```
calicoctl apply -f np/np-05.yaml
# проверяем.

# FROM app1 TO app2  
#
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# curl: (7) Failed to connect to service-app1-pod1.app1 port 81: Operation timed out

# FROM default TO app1 (запрещено политикой выше)
curl http://service-app1-pod1.app1.svc:81
# curl: (7) Failed to connect to service-app1-pod1.app1 port 30180: Connection refused
```

### Dev окружение
```
# Удалите все политики, которые были добавлены ранее.

calicoctl delete -f np-03.yaml 
calicoctl delete -f np-04.yaml
calicoctl delete -f np-05.yaml

# Достаточно распространённая ситуация - выделение набора namespaces в кластере для разработчиков. В этом случае нам 
# потребуется разрешить беспрепятственное хождение пакетов между этими namespaces, но запретить исходящий трафик.

# В calico сетевые политики применяются к различным Endpoints (термин calico). Эти endpoints в политках выбираются 
# стандартным для kubernetes методом - при помощи labels. Соответственно, если мы хотим в политиках использовать
# endpoints, расположенные в определённых namespaces, мы должны пометить эти namespaces.

# Предположим, что namespaces app1 и app2 выделены разработчикам. Пометим их при помощи labels:

kubectl label namespace app1 developer=company1
kubectl label namespace app2 developer=company1

# Добавим сетевую политику:
```
```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: access-company1
spec:
  types:
    - Ingress
    - Egress
  namespaceSelector: 'developer == "company1"'
  ingress:
    - action: Allow
      source:
        namespaceSelector: 'developer == "company1"'
  egress:
    - action: Allow
      destination:
        namespaceSelector: 'developer == "company1"'
```
```
#  внимание на то, что при ограничении исходящего трафика всегда необходимо разрешать обращение к DNS.
```
```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: access-company1-to-dns
spec:
  types:
    - Egress
  namespaceSelector: 'developer == "company1"'
  egress:
    - action: Allow
      protocol: UDP
      destination:
        nets:
          - 169.254.25.10/32
        ports:
          - 53
    - action: Allow
      protocol: TCP
      destination:
        nets:
          - 169.254.25.10/32
        ports:
          - 53
    - action: Allow
      destination:
        services:
          name: kubernetes
          namespace: default
```
```
# Применим политики:

calicoctl apply -f np-06.yaml 
calicoctl apply -f np-07.yaml 

# Проверяем работу политики (Всё работает, но только внутри namespaces.)

http://192.168.1.171:30180/ 
# 504 Gateway Time-out

# FROM app1 TO app2  
#
curl http://service-app2-pod1.app2:81
# <p>Простая тестовая страница app2-pod1</a>.
curl http://service-app2-pod2.app2:81
# <p>Простая тестовая страница app2-pod2</a>.

# FROM app2 TO app1  
#
curl http://service-app1-pod1.app1:81
# <p>Простая тестовая страница app1-pod1</a>.

# FROM default TO app1 (запрещено политикой выше)
curl http://service-app1-pod1.app1.svc:81
# curl: (7) Failed to connect to service-app1-pod1.app1 port 30180: Connection refused

# Добавить разрешение хождения из-за пределов кластера.
```
```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy      # Глобальная политика 
metadata:
  name: access-to-company1-from-inet
spec:
  types:
    - Ingress
  namespaceSelector: 'developer == "company1"'
  ingress:
    - action: Allow
      source:     # Доступ с подов  ingress
        selector: 'app.kubernetes.io/name == "ingress-nginx"'
```

```
calicoctl apply -f np/np-08.yaml 


http://192.168.1.171:30180/ 
# Тестовая страница app1-pod1

# FROM default TO app1 (запрещено политикой выше)
curl http://service-app1-pod1.app1.svc:81
# curl: (7) Failed to connect to service-app1-pod1.app1 port 30180: Connection refused

# Объеденить все эти политики можно объединить в одну:
```
```yaml
apiVersion: projectcalico.org/v3
kind: GlobalNetworkPolicy
metadata:
  name: access-company1
spec:
  types:
    - Ingress
    - Egress
  namespaceSelector: 'developer == "company1"'
  ingress:
    - action: Allow
      source:
        namespaceSelector: 'developer == "company1"'
    - action: Allow
      source:
        selector: 'app.kubernetes.io/name == "ingress-nginx"'
  egress:
    - action: Allow
      destination:
        namespaceSelector: 'developer == "company1"'
    - action: Allow
      protocol: UDP
      destination:
        nets:
          - 169.254.25.10/32
        ports:
          - 53
    - action: Allow
      protocol: TCP
      destination:
        nets:
          - 169.254.25.10/32
        ports:
          - 53
    - action: Allow
      destination:
        services:
          name: kubernetes
          namespace: default
```

```
calicoctl delete -f np/np-06.yaml
calicoctl delete -f np/np-07.yaml
calicoctl delete -f np/np-08.yaml
calicoctl apply -f np/np-09.yaml
```
