##### INSTALL

```
cert-manager - утилита для управления сертификатами.
Установка argocd
Настраиваем ingress для доступа.
Установка CLI
Пароль админа
Добавление пользователя
```
###### cert-manager
```bash 
# Создание namespace argocd
kubectl create namespace argocd

# Создаем ключ (лежит или в ssl или pki) 
# необходим для подписания сертификатов используем k8s сертификат 

# kubectl -n argocd create secret tls kube-ca-secret \
# --cert=/etc/kubernetes/ssl/ca.crt \
# --key=/etc/kubernetes/ssl/ca.key

kubectl -n argocd create secret tls kube-ca-secret \
--cert=/etc/kubernetes/pki/ca.crt \
--key=/etc/kubernetes/pki/ca.key

# Новая версия не взлетела 
# kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.20.2/cert-manager.yaml

kubectl apply -f https://github.com/jetstack/cert-manager/releases/download/v1.14.0/cert-manager.yaml

# Namespace cert-manager создаётся автоматически
```
###### Установка argocd
```bash

# Установка последней версии с сайта 
https://argo-cd.readthedocs.io/en/stable/

# kubectl apply -n argocd --server-side --force-conflicts -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
                                     
# Установка с указанием версии                                     
# curl -o install.yaml https://raw.githubusercontent.com/argoproj/argo-cd/v2.0.1/manifests/install.yaml

# Устанвока в ручном режиме 
# Исходный файл разбит на два: argo-1.yaml и argo-2.yaml. В первом файле находятся CRD. Его менять не будем.
# Во втором файле будем изменять аргументы командной строки.
```
```yaml
# что менялось
apiVersion: apps/v1
kind: Deployment
# ---
  name: argocd-server
# ---

containers:
      - command:          # для запуска контейнера 
        - argocd-server
        - --staticassets
        - /shared/app
        - --insecure     # добавляется данный параметр
        # тк argocd при запуске использует самоподписанный сертификат и доступ к нему планируется не через nodeport
        # а через ingress (терминация ssl на ingress)
        
        # праметы ниже можно раскоментиь если в однром домене будет приклад определяться по разным пустям 
        # www.my-domen.ru/grafana
        # www.my-domen.ru/argocd 
        # 
        # - --basehref
        # - /argocd     
    

```

``` bash 
kubectl -n argocd apply -f ./argocd/argo-1.yaml
kubectl -n argocd apply -f ./argocd/argo-2.yaml


###### Установка CLI

```bash
curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/v2.0.1/argocd-linux-amd64
chmod +x /usr/local/bin/argocd
argocd version
```

###### Получаем доступ 
```bash
kubectl -n argocd get service

# NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)                      AGE
# argocd-dex-server       ClusterIP   10.233.1.44     <none>        5556/TCP,5557/TCP,5558/TCP   4h34m
# argocd-metrics          ClusterIP   10.233.24.13    <none>        8082/TCP                     4h34m
# argocd-redis            ClusterIP   10.233.36.175   <none>        6379/TCP                     4h34m
# argocd-repo-server      ClusterIP   10.233.62.110   <none>        8081/TCP,8084/TCP            4h34m
# argocd-server           ClusterIP   10.233.7.62     <none>        80/TCP,443/TCP               4h34m
# argocd-server-metrics   ClusterIP   10.233.39.95    <none>        8083/TCP                     4h34m

# открываем порт 
# kubectl port-forward [resource-type]/[resource-name] [local-port]:[resource-port]
# resource-type — тип ресурса (например, pod, svc, deployment)

kubectl port-forward -n argocd service/argocd-server --address 0.0.0.0 8888:443

https://192.168.1.171:8888


# Второй вариант через NodePort
kubectl pply -f ./argocd/node_port_argocd.yaml

http://192.168.1.171:30443

# Пароль админа
```bash
# Добавим в /etc/hosts имя argocd.kube.local

# AgroCD - используем локальных пользователей 
# конфигурацию хранит в secret или configmap

# Secrets\argocd-initial-admin-secret
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d ; echo

# argocd login argocd.kube.local:31443 --grpc-web
# argocd account update-password --grpc-web

argocd login 192.168.1.171:30443 --grpc-web
WARNING: server is not configured with TLS. Proceed (y/n)? y
Username: admin
Password:
'admin:login' logged in successfully
Context '192.168.1.171:30443' updated

# Креды также можно посмотреть здесь cat ~/.argocd/config
# изменить установленый пароль
argocd account update-password --grpc-web

# Добавление пользователя, репы и добавить ему права
# через ГУИ пользоваетелй добавить нельзя 

kubectl -n argocd apply -f ./argocd/03-argocd-cm.yaml
kubectl -n argocd apply -f ./argocd/04-argocd-rbac-cm.yaml

# Посмотреть список пользователей в системе 
argocd account list --grpc-web

# NAME   ENABLED  CAPABILITIES
# admin  true     login
# const  true     apiKey, login

# сменить пароль
argocd account update-password --account const --grpc-web

# *** Enter current password:        <---- admin password
# *** Enter new password:
# *** Confirm new password:
# Password updated

# Логинимся новым пользователем в систему
argocd login argocd.const.local:30443 --grpc-web
argocd cluster list
# SERVER                          NAME        VERSION  STATUS  MESSAGE
# https://kubernetes.default.svc  in-cluster

# Заходим в WEB интерфейс

http://192.168.1.171:30443

```
###### Добавление project
```bash
# project - заливает на кластер базовые утилиты и следит за ними 
# найти можно в CRD (k8s dashboard)
kubectl -n argocd apply -f ./argocd/05-project-system.yaml

# добавить приложения в argocd через WEB
# приложение находится тут 
# https://github.com/j1nn33/study/tree/master/K8S/argocd/01-clusterapp/01-base

# NEW APP
# Application Name        base
# Project Name            system-utils
# SYNC POLICY             MANUAL
# Repository URL 
# Path                    K8S/argocd/01-clusterapp/01-base
# Cluster URL             https://kubernetes.default.svc
# Namespace               


# добавить приложения в argocd через manifest
./study/K8S/argocd/applications/01-base.yaml

# применить его 
kubectl apply -f ./argocd/applications/01-base.yaml
```















```bash 
# ----------------------------------------------------
```
###### ingress для доступа.


```bash
# настройка сертификата 
# dnsNames:
# - argocd.kube.local

kubectl apply -f ./argocd/00-certs.yaml


#-----------------------------------------------------
##### Не заработало
# доступ к ingress черер nodeport 
# http   :31080
# https  :31443

# 01-ingress-controller_single_node.yaml
# kubectl apply -f ./argocd/01-ingress-controller.yaml
# смотрим что он завелся namespae ingress
#-----------------------------------------------------

# заработало 
curl -L -o ingress-nginx.yaml https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.1/deploy/static/provider/cloud/deploy.yaml
kubectl apply -f ./argocd/ingress-nginx.yaml

# доступ к ingress черер nodeport 
# http   :31080
# https  :31443

kubectl apply -f ./argocd/nodePort.yaml


# Добавляем ingress
# правим если нужно - argocd.kube.local
kubectl apply -f 02-ingress.yaml

```
