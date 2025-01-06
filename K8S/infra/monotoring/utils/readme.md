```bash
# В кластере уже установлен 
# ingress controller (Over a NodePort Service)   
# Ingress Classes nginx
# ./K8S/tasks/kryukov/network/ingress.md

# Посмотреть порты на которых висит ingress-controllre 30180  30443
kubectl get service -ALL | grep ingress-nginx

# ingress-nginx          ingress-nginx-controller             NodePort    10.233.53.170   <none>        80:30180/TCP,443:30443/TCP   63m
# ingress-nginx          ingress-nginx-controller-admission   ClusterIP   10.233.62.16    <none>        443/TCP   

# В логах контейнера ingress-nginx-controller можно увидеть обращения 


# поэтому в  ./K8S/infra/monotoring/utils/ingress.yml
# 
# kubernetes.io/ingress.class: "nginx"
```