
#####  вывод сервиса наружу
##### 
###### - nodeport  ---> pod 
###### - metallb   ---> service (type loadbalancer)            --> pod
###### - metallb   ---> ngresscontroller (type loadbalancer)   --> pod 


##### Диагностика
```
kubectl describe 
kubectl get events
kubectl log  
```
###### связь deployment и service
```
service    <----->  pod
selector      =     label 
targetport    =     container POD
INGERSS (serviceport:80) = (port:80) SERVICE (targetport:3000) = (containerPort:3000) POD  
```
###### Связь компонентов 
```
1 POD ---> 2 Service & POD ---> 3 Ingress & Service

deployment & service - не связаны
----------------------------------
service  <---> pod 

sector      = label
target:Port = container pot
Servce:port - может быть любым тк ip service разные

в yaml файле 

label:port = target:port - должны совпадать

kubectl get pods --show-labels

ingres  
        service port 80 

           ||

        port 80
service
        target port 3000

           ||
Pod     container Port 3000           

----------------------------------
ingress       &   service
service port   =  port
service name   =  name
----------------------------------


ingres(port 80)  ----> service (clusterIP:80)
ingress ссылается на service приложения 
Важно 
  указываем на какой ingress-controller вешается ingress
  annotations:  
    kubernetes.io/ingress.class: "nginx-host"  

```
