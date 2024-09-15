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

kubectl get svc -A
# NAMESPACE              NAME                                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# ingress-nginx          ingress-nginx-controller             NodePort    10.233.53.170   <none>        80:30180/TCP,443:30443/TCP   9h
# ingress-nginx          ingress-nginx-controller-admission   ClusterIP   10.233.62.16    <none>        443/TCP                      9h

# когда устанавливаешь k8s на голое железо, внешний балансировщик отсутствует, поэтому службы не получают EXTERNAL-IP

```

####  ingress controller (Via the host network) 
```

```
