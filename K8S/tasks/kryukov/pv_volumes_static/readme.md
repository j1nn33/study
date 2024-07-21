##          Хранилища в кубере                             
######          - video                                    https://www.youtube.com/playlist?list=PLmxqUDFl0XM76Hnmsc2UDSvBT9Wf4W8Zl
######          - теория 
######          - prepare_cluster
######          - статический способ задания PV c локальным каталогом на ноде 
######          - настрйка NFS 
######          - статический способ задания PV с NFS


####  Теория 
```
- POD (указываем persistentVolumeClaim)
- PVC (persistentVolumeClaim) - запрос к K8S на выдачу 
- PV  (persistentVolume) - подключение физичкого хранилища к K8S (не привязан к namespace) 
     - статический 
     - динамическая 
- физическое хранилще (NFS, Ceph)
```

##### prepare_cluster
```
kubectl apply -f 00_prepare-cluster-volume.yaml
kubectl get all -o wide -n volumes-sample 

# Получить доступ 
kubectl -n volumes-sample apply -f 01_nodeport_nginx.yaml

kubectl -n volumes-sample get all -o wide
# NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE   SELECTOR
# service/openresty-srv                ClusterIP   10.233.63.159   <none>        80/TCP         70m   app=openresty
# service/service-nodeport-openresty   NodePort    10.233.12.87    <none>        80:30880/TCP   4s    app=openresty

http://192.168.1.171:30880/
# При наличии HA (когда разворачивался клатстер)
http://192.168.1.189:30880/

# Убрать за собой 

kubectl delete namespaces volumes-sample
```

##### статический способ задания PV
```
# - на ноде должен существовать каталог /opt/local-pv права 777
mkdir /opt/local-pv
chmod 777 /opt/local-pv/
vi /opt/local-pv/123.txt
# все измениения ототбражаются в каталоге пода или кталоге ноды 

# - ./K8S/tasks/kryukov/pv_volumes/02_static_local_pv.yaml
# - не указывается namespace тк это сущность кластера
# - используется локальная файловая система ноды кластера 
#
#   local:                  # определям что это локальная файловая система (каталог должен уже быть, он не создаестя при примении манифеста )
#     path: /opt/local-pv
#   nodeAffinity:           # опеделяем ноду где будте  persistentVolume
#     required:                            # на ноде есть label  kubernetes.io/hostname значение находится в списке  control1.kube.local
#       nodeSelectorTerms:                  
#       - matchExpressions:                 
#         - key: kubernetes.io/hostname     
#           operator: In                    
#           values:                        
#           # - worker2.kube.local         
#           - control1.kube.local

kubectl apply -f 02_static_local_pv.yaml
kubectl get pv

# NAME         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# test-local   1Gi        RWO            Retain           Available                          <unset>                          103s

# Retain    - политика высвобождения ресурос после удаления PV (удалить данные или оставить)
# Available - значит что еще никто не подлючился  Bound - подключен Released - освобожден


# запрос на выдачу (указывается namespace)
kubectl apply -f 03_claim_static_local_pv.yaml

kubectl -n volumes-sample get pvc
# NAME              STATUS   VOLUME       CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# claim-local-pvc   Bound    test-local   1Gi        RWO                           <unset>                 3m56s

kubectl get pv
# NAME         CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                            STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# test-local   1Gi        RWO            Retain           Bound    volumes-sample/claim-local-pvc                  <unset>                          11m
# Bound - статус сменился значит что pvc подключен к pv 

# развернем pod (хранилище будет добавлено в mountPath: /mnt/local)
kubectl apply -f 04_openresty_local.yaml

[root@openresty-local-75b7c9645f-wnjx8 /]# cat /mnt/local/123.txt 
```
##### настрйка NFS 
```
# ./K8S/infra/nfs/readme.md
# Создаем на сервере nfs каталог static-pv
mkdir /var/nfs-disk/static-pv
ls -lah /var/nfs-disk/
# drwxr-xr-x.  2 root root    6 Jun 18 12:25 static-pv

```
##### статический способ задания PV с NFS
```
# Указываем настроки nfs сервера и папки которую сервер шарит см ./K8S/infra/nfs/readme.md
# Посмотреть папку которую он шарит на nfs сервере /etc/exports
# persistentVolume  ./K8S/tasks/kryukov/pv_volumes_static/05_nfs_pv.yaml
# nfs: 
#    path: /var/nfs-disk/static-pv
#    server: 192.168.1.170

kubectl apply -f 05_nfs_pv.yaml

kubectl get pv
# NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# test-nfs   1Gi        RWX            Retain           Available                          <unset>                          2m4s


kubectl apply -f 06_claim_nfs_pv.yaml
kubectl -n volumes-sample get pvc
# NAME           STATUS   VOLUME     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
# claim-nfs-pv   Bound    test-nfs   1Gi        RWX                           <unset>                 57s

kubectl get pv
# NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                         STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
# test-nfs   1Gi        RWX            Retain           Bound    volumes-sample/claim-nfs-pv                  <unset>                          4m53s

kubectl apply -f 07_openresty_nfs.yaml

[root@openresty-67d6697746-6rclf /]# cat /mnt/nfs/tets.xt 

```

