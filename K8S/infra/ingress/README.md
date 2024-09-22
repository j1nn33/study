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
# в данном случае рассматривается работа в паре с ingress controller (Over a NodePort Service) на кластере 
# поэтому host-ingress-controller.yaml не содержит тех сущностей что были созданы во время создания ingress controller (Over a NodePort Service)   
# Разницу смотри ./K8S/tasks/kryukov/network/ingress.md

kubectl apply -f host-ingress-controller.yaml

# Для тестового кластера replicaset=1 
kubectl -n ingress-nginx get  pods
# NAME                                             READY   STATUS      RESTARTS        AGE
# ingress-nginx-admission-create-nsf45             0/1     Completed   0               34d
# ingress-nginx-admission-patch-fz69q              0/1     Completed   1               34d
# ingress-nginx-controller-f7587f845-5wt74         1/1     Running     1 (5d15h ago)   6d17h
# ingress-nginx-controller-host-6756b9c66c-wmp76   1/1     Running     0               5m7s

# Запускаем следующий ingress для примера (Openresty)

kubectl apply -f openresty_ingress_host.yml

Отличия от передыдущего openresty.yml

# cat openresty_ingress_host.yml
name: access-openresty-host
 spec:
  ingressClassName: nginx-host    - имя ingressClass указывали  ./K8S/tasks/kryukov/network/ingress/nodeport-ingress-controller.yaml - --ingress-class=nginx (строка 468)

http://192.168.1.171:280/
https://192.168.1.171:2443/

# Проверка портов 
netstat -tulpen | grep 80
# tcp        0      0 0.0.0.0:280             0.0.0.0:*               LISTEN      101        395404     66732/nginx: master
# tcp6       0      0 :::280                  :::*                    LISTEN      101        395395     66732/nginx: master

netstat -tulpen | grep 443
# tcp        0      0 0.0.0.0:2443            0.0.0.0:*               LISTEN      101        395410     66732/nginx: master
# tcp6       0      0 :::2443                 :::*          

# При проблемах смотрим логи ingress controller

"Configuration changes detected, backend reload required"
"New leader elected" identity="ingress-nginx-controller-f7587f845-2w4d7"
"Backend successfully reloaded"
"Initial sync, sleeping for 1 second"
Event(v1.ObjectReference{Kind:"Pod", Namespace:"ingress-nginx", Name:"ingress-nginx-controller-host-c4f6d77c9-7rvrv", UID:"8e624301-b5a2-48e2-a37e-0e9dedd21db6", APIVersion:"v1", ResourceVersion:"690321", FieldPath:""}): type: 'Normal' reason: 'RELOAD' NGINX reload triggered due to a change in configuration
{"time": "2024-09-22T11:01:23+00:00", "remote_addr": "", "x-forward-for": "192.168.1.37", "request_id": "907bbdacc44b8546632ba291358a696e", "remote_user": "", "bytes_sent": 129110, "request_time": 0.002, "status":200, "vhost": "192.168.1.171", "request_proto": "HTTP/2.0", "path": "/", "request_query": "", "request_length": 2062, "duration": 0.002,"method": "GET", "http_referrer": "", "http_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36", "namespace": "volumes-sample", "ingress_name": "access-openresty", "service_name": "openresty-srv", "service_port": "80" }

```
