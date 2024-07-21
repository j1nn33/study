##          Хранилища в кубере                             
######          - video                                    https://www.youtube.com/playlist?list=PLmxqUDFl0XM76Hnmsc2UDSvBT9Wf4W8Zl
######          - теория 
######          - prepare_cluster
######          - настрйка NFS
######          - настройка provisioner через helm
######          - настройка provisioner ручной вариант
######          - динамический способ задания PV с NFS

####  Теория 
```
- POD (указываем persistentVolumeClaim)
- PVC (persistentVolumeClaim) - запрос к K8S на выдачу 
- PV  (persistentVolume) - подключение физичкого хранилища к K8S (не привязан к namespace) 
     - статический 
     - динамическая 
- Provisioner - реагируте в системе на событя (создание, удаление ...) PVC и отдает команды на (создание, удаление ...) PV
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
##### настрйка NFS 
```
# ./K8S/infra/nfs/readme.md
# Создаем на сервере nfs каталог auto-pv
mkdir /var/nfs-disk/auto-pv
```
##### настройка provisioner через helm
```
# Проект "Kubernetes NFS-Client Provisioner"
https://github.com/kubernetes-sigs/nfs-subdir-external-provisioner

helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=192.168.1.170 \
    --set nfs.path=/var/nfs-disk/auto-pv
```
##### настройка provisioner ручной вариант
```
# Создаем системный namespace nfs-client с label app: nfs-client-provisioner для provisioner 
kubectl apply -f 02_nfs_ns.yaml

# Создаине rbac
#   - создание service account        - nfs-client-provisioner
#   - создание ClusterRole            - nfs-client-provisioner-runner (сущность кластера )
#   - создание ClusterRoleBinding     - run-nfs-client-provisioner bind к ClusterRole (nfs-client-provisioner-runner)
#   - создание Role                   - сущность namespace (где применяется) leader-locking-nfs-client-provisioner
#   - создание RoleBinding            - 
kubectl apply -f 03_rbac.yaml

# StorageClass (что-то типа labal, только с расширенными правами )
# provisioner: kube.local/nfs     # must match deployment's env PROVISIONER_NAME
# archiveOnDelete: "false" - не сохранять данные при удалении       
kubectl apply -f 04_class.yaml

# deployment самого provisioner 
#          env:
#            - name: PROVISIONER_NAME        - на какие классы реагировать
#              value: kube.local/nfs
#            - name: NFS_SERVER
#              value: 192.168.1.170
#            - name: NFS_PATH
#              value: /var/nfs-disk/auto-pv  - внутри этой директории provisioner будет создавать директории
#      volumes:                              - указываем параметы nfs сервера
#        - name: nfs-client-root
#          nfs:
#            server: 192.168.1.170
#            path: /var/nfs-disk/auto-pv
```
##### динамический способ задания PV с NFS
```
# Создем PVC (persistentVolumeClaim) - запрос к K8S на выдачу 
# volume.beta.kubernetes.io/storage-class: "managed-nfs-storage"
# managed-nfs-storage - имя StorageClass описанного в 04_class.yaml
kubectl apply -f 06_openresty_pvc.yaml

kubectl -n volumes-sample get pvc
# NAME              STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS          VOLUMEATTRIBUTESCLASS   AGE
# openresty-claim   Bound    pvc-00583c30-9c97-42cf-8801-36ab92c0aff7   1Mi        RWX            managed-nfs-storage   <unset>                 7m16s

# на сервере NFS  ls -lah /var/nfs-disk/auto-pv/
# drwxrwxrwx. 2 root root  6 Jun 18 19:21 volumes-sample-openresty-claim-pvc-00583c30-9c97-42cf-8801-36ab92c0aff7
# 
# namespace      pvc             volume 
# volumes-sample-openresty-claim-pvc-00583c30-9c97-42cf-8801-36ab92c0aff7

# ЕСЛИ удалить pvc то удаляется pv и каталог с сервера NFS
kubectl delete -f 06_openresty_pvc.yaml 

# Создаем deployment openresty c mountPath: /var/log/nfs
kubectl apply -f 07_openresty.yaml
```



