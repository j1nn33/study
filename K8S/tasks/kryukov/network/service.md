##          Service
######          - video                   
######          - имена портов                    
######          - Endpoint
######          - Сервисы без селекторов
######          - Headless Service
######          - ExternalName
######          - 
######          - 
######          - 

#### video
```
https://www.youtube.com/watch?v=OWUOHM_08mc&list=PLmxqUDFl0XM6wDtlCkwdjU55z_WeBgBsZ&index=8
https://www.youtube.com/watch?v=OHBv_OdjVIU&list=PLmxqUDFl0XM6wDtlCkwdjU55z_WeBgBsZ&index=9
https://www.youtube.com/watch?v=9SS-0GeH2ho&list=PLmxqUDFl0XM6wDtlCkwdjU55z_WeBgBsZ&index=11

```
#### имена портов
```
# В описании deployment имя порта (к протам лучше обращаться по именам)
# Это удобно, если ссылаетесь на поды, у которых определены разные номера портов, но под одним именем.
# например старый функционал на java (port1) новый на Go (port2) и на них надо загонять трафик 
# ./K8S/tasks/kryukov/network/sevice/01-deployment.yaml
---
ports:
 - containerPort: 8080
   name: tomcat
   protocol: TCP
---
# Обрацение к pod про имени порта задаестя в srvice 
# ./K8S/tasks/kryukov/network/sevice/02-service.yaml
---
ports:
  - protocol: TCP
    port: 80
    targetPort: tomcat
---
```
#### Endpoint
```
# заполняются endpoint когда pod пройдет readnes probe
# связь между service и pod 
# получить endpoint
kubectl get ep
kubectl get -n volumes-sample ep
# получить описание endpoint 
kubectl get ep tomcat-main -o yaml

kubectl -n volumes-sample  get svc
# NAME                         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
# openresty-srv                ClusterIP   10.233.36.175   <none>        80/TCP         18d
# service-nodeport-openresty   NodePort    10.233.62.71    <none>        80:30880/TCP   18d

kubectl get -n volumes-sample ep
# NAME                         ENDPOINTS         AGE
# openresty-srv                10.233.66.10:80   18d
# service-nodeport-openresty   10.233.66.10:80   18d

kubectl get pods -ALL -o wide
# volumes-sample         openresty-758cd79c6-m299v   10.233.66.10    control1.kube.local  

# Посмотреть nat преобразование

ipvsadm -L -n
# IP Virtual Server version 1.2.1 (size=4096)
# Prot LocalAddress:Port Scheduler Flags 
#   -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
# TCP  10.233.36.175:80 rr
#   -> 10.233.66.10:80              Masq    1      0          0
# TCP  10.233.62.71:80 rr
#   -> 10.233.66.10:80              Masq    1      0          0


```
#### Сервисы без селекторов
```
# Сервисы без селекторов обычно используются для обращения за пределы кластера по ip адресу к какому либо приложению (база данный или что-то еще )
# - создание сервиса для mail.ru 
./K8S/tasks/kryukov/network/sevice/03-service-mail-ru.yaml
# - так же необходимо создать endpoint 
./K8S/tasks/kryukov/network/sevice/04-endpoint-mail-ru.yaml
# Определение endpoint. Имя сервиса и endpoint должны совпадать.

curl mail-ru:8080
```
#### Headless Service
```
# На примере StatefullSet ./K8S/tasks/kryukov/network/sevice/05-nexus.yaml  (манифест создает два сервиса Headless и сервис на конкретный pod StatefullSet)
# обращаться к сервису можно только по его имени 
# Конструкции headless сервиса нельзя использовать при обращении к конкретному поду, например в ingress. 
# Если очень надо то для каждого пода создать отдельный сервис по метку типа: statefulset.kubernetes.io/pod-name
kubectl get svc
# NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)
# nexus         ClusterIP   None            <none>        8081/TCP

dig nexus.default.svc.cluster.local
# nexus.default.svc.cluster.local. 5 IN   A       10.234.9.3
# nexus.default.svc.cluster.local. 5 IN   A       10.234.8.199

# Поскольку не создаётся виртуальный ip сервиса, т.е. не создаётся NAT преобразование.
# Таким образом, если работе вашего приложения противопоказаны NAT преобразования – используйте headless сервисы.
```
#### ExternalName
```
# Обращеие к внешим ресурсам не по имени сервиса 
# Сервис типа ExternalName добавляет запись типа CNAME во внутренний DNS сервер Kubernetes.
# Для этого сервиса не создаётся endpoint
# ./K8S/tasks/kryukov/network/sevice/06-external-name.yaml

kubectl get svc
# NAME          TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)
# mail-ru       ExternalName   <none>          mail.ru       <none>

```
