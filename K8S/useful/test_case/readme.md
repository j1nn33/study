## Тестовые кейсы 


###### Deployment      (создание и откат версии nginx)
###### Service         (доступ к ngix)
###### NodePort        (доступ к ngix)
###### Volumes         (доступ к ngix)
######     - emptyDir          (доступ к ngix)
######

###### убрать за собой 
```
# Deployment, Service, NodePort
kubectl delete deployment test-deployment-nginx
kubectl delete service test-service-nginx
kubectl delete service test-service-nodeport-nginx

# Volumes
kubectl delete namespace test-volumes-sample 


# kubectl delete deployment openresty -n volumes-sample
# kubectl get all -o wide -n test-volumes-sample 
```
###### запуск
```
cd ./K8S/useful/test_case
```

#### Deployment 
###### создание и откат версии nginx с использованием Deployment 
```
kubectl apply -f 00-test-deployment-nginx.yaml
kubectl get all -o wide

# NAME                                       READY   STATUS    RESTARTS   AGE   IP              NODE                 NOMINATED NODE   READINESS GATES
# pod/test-deployment-nginx-5bd445f7-2mtzw   1/1     Running   0          36s   10.233.109.70   worker3.kube.local   <none>           <none>
# pod/test-deployment-nginx-5bd445f7-6rbb5   1/1     Running   0          36s   10.233.78.135   worker1.kube.local   <none>           <none>
# pod/test-deployment-nginx-5bd445f7-snt8m   1/1     Running   0          36s   10.233.81.72    worker2.kube.local   <none>           <none>
# 
# NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE   SELECTOR
# service/kubernetes   ClusterIP   10.233.0.1   <none>        443/TCP   18d   <none>
# 
# NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES         SELECTOR
# deployment.apps/test-deployment-nginx   3/3     3            3           36s   nginx        nginx:1.14.2   app=test-nginx
# 
# NAME                                             DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES         SELECTOR
# replicaset.apps/test-deployment-nginx-5bd445f7   3         3         3       36s   nginx        nginx:1.14.2   app=test-nginx,pod-template-hash=5bd445f7

```
###### Обновление версии nginx 1.14.2 --> 1.16.1
```
vim 00-test-deployment-nginx.yaml
---
image: nginx:1.16.1
---
kubectl apply -f 00-test-deployment-nginx.yaml

kubectl get all -o wide
---
# NAME                                               DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES         SELECTOR
# replicaset.apps/test-deployment-nginx-5bd445f7     0         0         0       15m   nginx        nginx:1.14.2   app=test-nginx,pod-template-hash=5bd445f7
# replicaset.apps/test-deployment-nginx-7cb9c9d548   3         3         3       34s   nginx        nginx:1.16.1   app=test-nginx,pod-template-hash=7cb9c9d548
---

# Посмотреть статус развертывания deployment
kubectl rollout status deployment.apps/test-deployment-nginx

# Отменить deployment
kubectl rollout undo deployment.apps/test-deployment-nginx

# История deployment
kubectl rollout history deployment.apps/test-deployment-nginx

# Откатиться до номера ревизии
kubectl rollout undo deployment.apps/test-deployment-nginx --to-revision=3

```

#### Service 
###### доступ к nginx 
```
kubectl apply -f 01-test-service-clusterip-nginx.yaml

kubectl get all -o wide
# NAME                                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE   SELECTOR
# service/test-service-clusterip-nginx   ClusterIP   10.233.41.81   <none>        8080/TCP   60s   type=test-front

curl 10.233.41.81:8080

```
#### NodePort 
###### доступ к nginx 
```
kubectl apply -f 02-test-nodeport-nginx.yaml
kubectl get all -o wide

# NAME                                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE   SELECTOR
# service/test-service-nodeport-nginx   NodePort    10.233.34.36   <none>        8080:30090/TCP   37s   type=test-front

curl 192.168.1.171:30090

http://192.168.1.189:30090/
http://192.168.1.17[1-7]:30090/ 
```

#### Volumes
###### подготовка (создание namespace, service) 
```
kubectl apply -f 03-test-prepare-cluster-volume.yaml
kubectl get all -o wide -n test-volumes-sample
kubectl get all -ALL -o wide | grep volumes

# Убрать за собой
kubectl delete namespaces test-volumes-sample
```
####  - emptyDir 
###### в поде определяется init контейнер и создает в volume «empty-volume» файл «init-file»
###### запускается основной контейнер в файловой системе которого уже доступен файл «init-file»
###### второй контейнер внутри пода подключется к volume 
###### разворачивается NodePort для доступа снаружи   
```
kubectl apply -f 04-test-volume-emptydir.yaml

http://192.168.1.189:30090/
http://192.168.1.17[1-7]:30090/ 

kubectl get all -o wide -n test-volumes-sample                                                                                                                                             
# 
# NAME                                                 READY   STATUS    RESTARTS   AGE   IP              NODE                 NOMINATED NODE   READINESS GATES
# pod/test-volume-emptydir-openresty-75fd977f5-jxlxt   2/2     Running   0          13m   10.233.78.141   worker1.kube.local   <none>           <none>
# 
# NAME                                             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE   SELECTOR
# service/test-openresty-srv                       ClusterIP   10.233.14.80    <none>        80/TCP         29m   app=test-openresty
# service/test-service-nodeport-volume-openresty   NodePort    10.233.45.144   <none>        80:30080/TCP   28m   app=test-openresty
# 
# NAME                                             READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS         IMAGES                                          SELECTOR
# deployment.apps/test-volume-emptydir-openresty   1/1     1            1           27m   openresty,centos   openresty/openresty:centos-rpm,centos:centos8   app=test-openresty
# 
# NAME                                                        DESIRED   CURRENT   READY   AGE   CONTAINERS         IMAGES                                          SELECTOR
# replicaset.apps/test-volume-emptydir-openresty-75fd977f5    1         1         1       13m   openresty,centos   openresty/openresty:centos-rpm,centos:centos8   app=test-openresty,pod-template-hash=75fd977f5

kubectl -n test-volumes-sample exec test-volume-emptydir-openresty-75fd977f5-jxlxt -it -c openresty -- bash
# -c openresty - обратиться к определенному контейнеру в поде 
# [root@test-volume-emptydir-openresty-75fd977f5-jxlxt /]# ls /empty/
# init-file
# vi /empty/test.txt

kubectl -n test-volumes-sample exec test-volume-emptydir-openresty-75fd977f5-jxlxt -it -c centos -- bash
# [root@test-volume-emptydir-openresty-75fd977f5-jxlxt /]# ls /empty/
# init-file
# cat /empty/test.txt
#  curl http://localhost/  

```