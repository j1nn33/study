# Сетевая связность и пропускная способность

#### iperf

```
kubectl apply -f iperf3-deployment.yaml

kubectl get pods -o wide
```
###### NAME                                READY   STATUS    RESTARTS   AGE   IP              NODE                 NOMINATED NODE   READINESS GATES
###### iperf3-deployment-685cf6b8d-6cn7b   1/1     Running   0          88s   10.233.109.68   worker3.kube.local   <none>           <none>
###### iperf3-deployment-685cf6b8d-gwpnf   1/1     Running   0          88s   10.233.78.132   worker1.kube.local   <none>           <none>
###### iperf3-deployment-685cf6b8d-t6fts   1/1     Running   0          88s   10.233.81.68    worker2.kube.local   <none>           <none>

###### запустить iperf в одном из подов, в режиме сервера:

```
# kubectl exec -it <pod-name> -- iperf3 -s -p 12345

kubectl exec -it pod/iperf3-deployment-685cf6b8d-6cn7b -- iperf3 -s -p 12345

# -----------------------------------------------------------
# Server listening on 12345
# -----------------------------------------------------------
```
###### другой сессии терминала нужно запустить Iperf в режиме клиента, и подключится из этого пода к серверу

```
# kubectl exec -it <pod-name> -- iperf3 -c <pod-ip_server> -p 12345

kubectl exec -it pod/iperf3-deployment-685cf6b8d-gwpnf -- iperf3 -c 10.233.109.68 -p 12345
# Connecting to host 10.233.109.68, port 12345
# [  4] local 10.233.78.132 port 51730 connected to 10.233.109.68 port 12345
# [ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
# [  4]   0.00-1.00   sec   723 MBytes  6.06 Gbits/sec  541    597 KBytes

```
###### Eсли при тестировании наблюдаются потери пакетов, то :
######    - Неисправности "железа" (CRC ошибки NIC проблемы с коммутаторами)
######    - Не правильно настроенный межсетевой экран
######    - Не правильно настроенный протокол (например MTU)

#### CRI 
###### CRI (Docker\containerd) отвечает за запуск контейнеров. 


```
crictl pull docker.io/library/busybox:latest

crictl ps
crictl inspect <CONTAINER_ID>

```

#### CNI  
###### Kubelet отправляет инструкции CNI, как присоединить сетевой интерфейс и настроить сеть для Пода.
###### CNI плагин (например Calico)- обязанности: аллоцировать и назаначять уникальные IP адреса для Подов и добавлять маршруты в кластере Kubernetes для каждого IP адреса Пода.
###### Категории в сетевой модели CNI: flat networks и overlay networks. 
######     - flat networks использует IP из сети кластера, для чего обычно требуется большое количество свободных адресов.
######     - В сетях overlay, драйвер CNI создает свою сеть в Kubernetes, и затем использует кластерную сеть (которая называется underlay network) для передачи пакетов.
###### kubelet читает конифиг CNI из директории /etc/cni/net.d/ и ожидает найти бинарный файл CNI в директории /opt/cni/bin/

#### Iptables
```
sudo iptables -t nat -L KUBE-SERVICES
```

#### DNS, L4/L7 CoreDNS
###### CoreDNS создает запись следующего формата: 
######    FQDN имя сервиса
######       [service-name].[namespace-name].svc.cluster.local
######       nginx.default.svc.cluster.local            Сервис, который называется nginx в пространстве имен default
######    FQDN имя для простого пода:
######    pod-ip-address.namespace-name.pod.cluster.local
######    10-233-79-186.default.pod.cluster.local

###### Kubespray ставит следующие компоненты системы:
######     - coredns – основной DNS сервер, отвечающий за разрешение имен внутри кластера Kubernetes.
######     - nodelocaldns – кеширующий DNS сервер. По одному на каждую ноду кластера. Bыполнен в виде daemonSet. 
######     - dns-autoscaler – приложение, автоматически увеличивающее или уменьшающее количество подов coredns в кластере (https://github.com/kubernetes-sigs/cluster-proportional-vertical-autoscaler).
######     - Для доступа и распределения запросов между подами coredns, создан соответствующий сервис. Cервис – это набор правил NAT преобразований на каждой ноде кластера.

###### При запуске pod, kubelet сохраняет в контейнере файл /etc/resolv.conf. B качестве nameserver там будет указан CoreDNS. 
```
cat /etc/resolv.conf
search default.svc.cluster.local svc.cluster.local cluster.local
nameserver <ip-CoreDNS>
options ndots:5
```
##### Сервис kube-dns подключается к развертыванию (Deployment) CoreDNS: <ip-CoreDNS> 10.233.0.10
```
kubectl -n kube-system get services

# NAME       TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)                  AGE
# kube-dns   ClusterIP   10.233.0.10   <none>        53/UDP,53/TCP,9153/TCP   10d
```
#### dnstools (dig, nslookup, curl, ping)
###### запустить под для тестирования DNS
```
kubectl apply -f dnstools.yaml

kubectl get pods dnstools
```
###### или
```
kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools
```
###### Запуск на конктретной ноде
```
kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools \
                --overrides='{"apiVersion": "v1", "spec": {"nodeSelector": { "kubernetes.io/hostname": "worker3.kube.local" }}}'
```
#### Отладка DNS
```
kubectl get pods -o wide -A | grep dns

kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools

# проверка ip nodelocal-dns
cat /etc/resolv.conf
search default.svc.cluster.local svc.cluster.local cluster.local kube.local
nameserver 169.254.25.10

# проверка coredns/kube-dns (находится в kube-system namespace) coredns резолвится по kube-dns
host coredns.kube-system.svc.cluster.local
host kube-dns.kube-system.svc.cluster.local
# kube-dns.kube-system.svc.cluster.local has address 10.233.0.10
host kube-dns.kube-system
```
###### Проверяем kubernetes

```
kubectl get service
# NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
# kubernetes   ClusterIP   10.233.0.1   <none>        443/TCP   10d
```
###### Важно проверить на каждой ноде 
```
kubectl get nodes
```
######  kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools \
######                 --overrides='{"apiVersion": "v1", "spec": {"nodeSelector": { "kubernetes.io/hostname": "<node_name>" }}}'
```
kubectl run -it --rm --restart=Never --image=infoblox/dnstools:latest dnstools \
                --overrides='{"apiVersion": "v1", "spec": {"nodeSelector": { "kubernetes.io/hostname": "worker3.kube.local" }}}'
host kubernetes
# kubernetes.default.svc.cluster.local has address 10.233.0.1

```

###### проверить L4\L7 соединение между Подами, порты и доступ в Интернет из кластера:
```
kubectl exec -i -t dnstools -- ping google.com -c 4
# PING google.com (216.58.211.238): 56 data bytes
# 64 bytes from 216.58.211.238: seq=0 ttl=56 time=22.494 ms

kubectl exec -i -t dnstools -- nc -z -vv ya.ru 80

kubectl exec -i -t dnstools -- nc -z -vv ya.ru 8080
```
###### layer 7 HTTP API:
```
kubectl exec -i -t dnstools -- wget -qO- 216.58.211.238:80
kubectl exec -i -t dnstools -- wget -qO- google.com:80
```
###### Проверить разрешение доменных имен в кластере:
```
kubectl exec -i -t dnstools -- nslookup kubernetes.default

# Server:         169.254.25.10
# Address:        169.254.25.10#53
# 
# Name:   kubernetes.default.svc.cluster.local
# Address: 10.233.0.1


kubectl exec -i -t dnstools -- dig hello-world.default.svc.cluster.example.com
```
###### получить доступ к контейнеру с dnstools:
```
kubectl run --restart=Never -it --image infoblox/dnstools dnstools
```
###### Сделать снимок сетевого трафика DNS (UDP 53) в контейнере dnstools:
```
kubectl exec -it dnstools sh
dnstools# tcpdump -ni eth0 udp and port 53
```
###### проверить содержимое /etc/resolv.conf:
```
dnstools# cat /etc/resolv.conf
# nameserver 169.254.25.10   - определено в nodelocaldns_local_ip: 169.254.25.10   ./project/K8S/ansible/kubeadm/group_vars/k8s_cluster
# search default.svc.cluster.local svc.cluster.local cluster.local
# options ndots:5
```


#### ksniff
###### https://github.com/eldadru/ksniff
###### 
###### ksniff - это плагин kubectl, который использует tcpdump для захвата сетевого трафика.
###### Трафик в формате PCAP можно затем импортировать в Wireshark для последующего анализа.
###### Для установки ksniff лучше использовать krew - менеджер плагинов для kubectl:
###### 
###### kubectl krew install sniff
###### Инструкции по установке krew для разных ОС:
###### https://krew.sigs.k8s.io/docs/user-guide/setup/install
###### 
###### Ksniff устанавливается на пользовательской машине с настроенным kubectl.
###### При запуске ksniff использует эфемерный контейнер с tcpdump для подключения к нужному Поду. Для работы с PCAP файлами, на машине должен быть установлен Wireshark.
###### 
###### Интерфейс кsniff :
###### 
###### kubectl sniff <POD_NAME> [-n <NAMESPACE_NAME>] [-c <CONTAINER_NAME>] [-i <INTERFACE_NAME>] [-f <CAPTURE_FILTER>] [-o OUTPUT_FILE] [-l LOCAL_TCPDUMP_FILE] [-r REMOTE_TCPDUMP_FILE]
###### Следующая команда сохранит перехваченные tcpdump сететвые пакеты в файл out.pcap:
###### 
###### kubectl sniff -n <NAMESPACE> <POD_NAME> -p -f "port 80" -o out.pcap
###### В данном случае отправляем tcpdump инструкции - отслеживать только запросы POST протокола HTTP на порту 8080:
###### 
###### kubectl sniff -p <POD_NAME> -n <NAMESPACE> -f 'tcp dst port 8080 and (tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x504f5354)' -o - | tshark -r -
###### С помощью флагов --image и --tcpdump-image можно указывать кастомизированные образы Docker. Эта функция может быть использована для работы в закрытом контуре.
###### 
###### Kubeshark
###### https://docs.kubeshark.co
###### 
###### Инструкции по установке:
###### https://docs.kubeshark.co/en/install
###### 
###### Принцип работы похож на ksniff – для захвата трафика используется контейнер с tcpdump.
###### Кроме этого Kubeshark добавляет графический веб-интерфейс и ряд возможностей, которые доступены лишь в системах для анализа трафика класса enterprise.
###### 
###### С kubeshark можно в режиме реального времени отслеживать перемещение трафика (REST, gRPC, Kafka, AMQP и Redis) в кластере,
###### и визуализировать связи между Сервисами Kubernetes - https://docs.kubeshark.co/en/service_map