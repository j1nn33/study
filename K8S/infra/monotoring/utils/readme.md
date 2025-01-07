```bash
# В кластере уже установлен 
# ingress controller (Over a NodePort Service)  
# ./K8S/tasks/kryukov/network/ingress.md

# Ingress Classes = nginx
# поэтому в  ./K8S/infra/monotoring/utils/ingress.yml
# 
# kubernetes.io/ingress.class: "nginx"




# Посмотреть порты на которых висит ingress-controllre 30180  30443
kubectl get service -ALL | grep ingress-nginx

# ingress-nginx          ingress-nginx-controller             NodePort    10.233.53.170   <none>        80:30180/TCP,443:30443/TCP   63m

# В логах контейнера ingress-nginx-controller можно увидеть обращения (если что-то не то)

```
Доступы 
```
https://192.168.1.171:30443/prometheus/
https://192.168.1.171:30443/grafana/login
https://192.168.1.171:30443/vm/login
```
