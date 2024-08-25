## Настройка параметров пода 

###### Hostname и subdomain (имя появится только в /etc/hosts - PODA в DNS его не будет и снаружи оно будет не доступно )
```
spec:
  hostname: dns
  subdomain: tools
```
#### у контейнера будет установлено имя dns.tools.default.svc.cluster.local

######  /etc/hosts
###### Для добавления записей в файл /etc/hosts контейнеров пода 
```
hostAliases:
        - ip: 8.8.8.8
          hostnames:
            - dns.google.local
            - dns8.google.local
        - ip: 8.8.4.4
          hostnames:
            - dns4.google.local
```
###### cat /etc/hosts
###### 8.8.8.8 dns.google.local dns8.google.local
###### 8.8.4.4 dns4.google.local

###### dns.google.local и dns8.google.local преобразовывваем в 8.8.8.8
###### dns4.google.local преобразовывваем 8.8.4.4

###### /etc/resolve
###### вместо стандартного файла /etc/resolvr.conf настроить свой собственный вариант
```
dnsPolicy: "None"
#  политика заставляет под игнорировать настройки DNS Kubernetes. Если используем dnsConfig 

dnsConfig:
  nameservers:
    - 8.8.8.8
    - 8.8.4.4
  searches:
     - kube.local
   options:
     - name: ndots
       value: "2"
```