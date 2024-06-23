# Удаление нод.

---
###### Удаление worker ноды
###### Сначала удаляем ноду из кластера.
```
kubectl delete node worker1.kryukov.local
```
###### Затем на самой ноде удалем приложения кластера.
```
kubeadm reset
```
###### После kubeadm reset containerd (или то что вы используете) не выключается.
###### Есть вероятность, что какие-то контейнеры продолжат работать.
###### Тут либо выключаем containerd, либо вручную останавливаем все запущенные контейнеры.

---
# Удаление control ноды

###### В случае control ноды, делаем всё так же как и в случае worker ноды. Но есть нюансы.
###### Если нода отключилась аварийно, удаление ноды из кластера при помощи 
###### kubectl будет недостаточно. Необходимо посмотреть состояние кластера etcd.
###### Если на упавшей ноде был один из серверов etcd, то его надо вручную удалить из кластера.

###### Дальнейшие действия показаны для установленного при помощи kubeadm etcd кластера. 
###### Переходим на рабочую control ноду. Смотрим на каком IP и порту слушает запросы etcd сервер
```
ss -nltp | grep 2379
```
###### Получаем название подов etcd сервера
```
kubectl -n kube-system get pods | grep etcd
```
###### Получаем список членов кластера etcd. Нам нужен id неработающего сервера.
```
kubectl -n kube-system exec etcd-control1.kube.local -- etcdctl \
  --endpoints '192.168.1.171:2379' \
  --cacert /etc/kubernetes/pki/etcd/ca.crt \
  --key /etc/kubernetes/pki/etcd/server.key \
  --cert /etc/kubernetes/pki/etcd/server.crt \
  member list

3290e2fc2debfa69, started, control1.kube.local, https://192.168.1.171:2380, https://192.168.1.171:2379, false
87cbf61d90994323, started, control2.kube.local, https://192.168.1.172:2380, https://192.168.1.172:2379, false
ae06f41d5e923036, started, control3.kube.local, https://192.168.1.173:2380, https://192.168.1.173:2379, false
```
###### Удаляем неработающий сервер из списка.
```
kubectl -n kube-system exec etcd-control1.kube.local -- etcdctl \
  --endpoints '192.168.1.171:2379' \
  --cacert /etc/kubernetes/pki/etcd/ca.crt \
  --key /etc/kubernetes/pki/etcd/server.key \
  --cert /etc/kubernetes/pki/etcd/server.crt \
  member remove ae06f41d5e923036
```


