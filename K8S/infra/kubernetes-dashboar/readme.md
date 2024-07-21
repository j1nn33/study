## Deploy and Access the Kubernetes Dashboard

###### https://v1-28.docs.kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/

###### Установка 
```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml

kubectl -n kubernetes-dashboard get all
 
# NAME                                             READY   STATUS    RESTARTS   AGE
# pod/dashboard-metrics-scraper-5657497c4c-hw2nd   1/1     Running   0          27s
# pod/kubernetes-dashboard-78f87ddfc-4j99m         1/1     Running   0          27s
# 
# NAME                                TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
# service/dashboard-metrics-scraper   ClusterIP   10.233.24.32   <none>        8000/TCP   27s
# service/kubernetes-dashboard        ClusterIP   10.233.48.89   <none>        443/TCP    27s
# 
# NAME                                        READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/dashboard-metrics-scraper   1/1     1            1           27s
# deployment.apps/kubernetes-dashboard        1/1     1            1           27s
# 
# NAME                                                   DESIRED   CURRENT   READY   AGE
# replicaset.apps/dashboard-metrics-scraper-5657497c4c   1         1         1       27s
# replicaset.apps/kubernetes-dashboard-78f87ddfc         1         1         1       27s
```

###### Получим порт на котором работают поды дашборда
```
kubectl -n kubernetes-dashboard describe service kubernetes-dashboard

# TargetPort:        8443/TCP
```

###### Получим снаружи 1 вариант Проборска портов
```
# kubectl port-forward -n <name_space> <pod_name> --address 0.0.0.0 8888:80
kubectl port-forward -n kubernetes-dashboard kubernetes-dashboard-78f87ddfc-g7c5h --address 0.0.0.0 8000:8443

# https://192.168.1.171:8000/#/login
```

###### Получим снаружи 2 вариант NodePort
###### cгенерируем/проверим содержимое в файла node_port_ks_dasboard.yaml на основе service kubernetes-dashboard
```
kubectl -n kubernetes-dashboard edit service kubernetes-dashboard
kubectl apply -f node_port_ks_dasboard.yaml
kubectl -n kubernetes-dashboard get service

# NAME                             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)         AGE
# dashboard-metrics-scraper        ClusterIP   10.233.24.32    <none>        8000/TCP        4m50s
# kubernetes-dashboard             ClusterIP   10.233.48.89    <none>        443/TCP         4m50s
# node-port-kubernetes-dashboard   NodePort    10.233.21.101   <none>        443:30800/TCP   13s


https://192.168.1.171:30800/#/login
```

###### Доступ к дашборду 
###### https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md

###### Создание пользователя и ролевой модели 
```
kubectl apply -f create_cred_ks-dasboard.yaml
```
######  Содание быстрого токена
```
kubectl -n kubernetes-dashboard create token admin-user
```
######  Содание long-lived Bearer Token 
```
kubectl apply -f token_for_dashboard.yaml
kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath={".data.token"} | base64 -d
```

###### Clean up 
###### Remove the admin ServiceAccount and ClusterRoleBinding.
```
kubectl -n kubernetes-dashboard delete serviceaccount admin-user
kubectl -n kubernetes-dashboard delete clusterrolebinding admin-user
```

