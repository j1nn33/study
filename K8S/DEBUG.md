
#####  вывод сервиса наружу
##### 
##### - nodeport  ---> pod 
##### - metallb ---> service (type loadbalancer) --> pod
##### - metallb ---> ngresscontroller (type loadbalancer) --> pod 
#####                 - service /prometey
##### 				-         / k8s

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


