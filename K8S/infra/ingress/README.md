## ingrees                              

######    - Теория    
######    - ingress controller (Over a NodePort Service)        
######    - ingress controller (Via the host network)   
######    -      

####    - Теория  
```
Описана ./K8S/tasks/kryukov/network/ingress.md

```
####   ingress controller (Over a NodePort Service)   
```
# сделать лейбы на ноды, чтобы igress-controller запускался только на них 

kubectl label nodes worker1.kube.local ingress-nginx-node=enable
kubectl label nodes worker2.kube.local ingress-nginx-node=enable

# запустить деплоймент (репликасет сделать 1 для тестового кластера)
# ./K8S/tasks/kryukov/network/ingress/nodeport-ingress-controller.yaml
kubectl apply -f nodeport-ingress-controller.yaml

# Посмотреть порты 
kubectl get service -ALL | grep ingress-nginx

# ingress-nginx          ingress-nginx-controller             NodePort    10.233.53.170   <none>        80:30180/TCP,443:30443/TCP   63m
# ingress-nginx          ingress-nginx-controller-admission   ClusterIP   10.233.62.16    <none>        443/TCP                      63m








```

####  ingress controller (Via the host network) 
```

```
