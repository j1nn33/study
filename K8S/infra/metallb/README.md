## metallb                              

######    - Теория   
######    - подготовка 
######    - Install      
######    - ingress (type loabalancer)
   

####    - Теория  
```
# Когда устанавливаешь k8s на голое железо, внешний балансировщик отсутствует, поэтому службы не получают EXTERNAL-IP
# поставим Metallb, который заменит нам внешний балансировщик

https://metallb.universe.tf/

# Поставляет некоторый ip адрес для сервивиса типа loadbalancer
# обратившись на этот ip получаем доступ к сервису loadbalancer

# Metallb - необходимо прдеостваить пул ip адресов 
# имеет 2 режима работы:
#   - layer 2 mode  
#   - in BGP mode  (для больших кластеров)

# Работать будет с сервисами типа loadbalancer

```
#### подготовка   

```
# Убедится, что KubeProxy запущен с параметром:
ipvs:
  strictARP: true

# ./K8S/ansible/kubeadm/roles/master/templates/kubeadm-config.j2

kubectl get configmap kube-proxy -n kube-system -o yaml | grep strictARP
      strictARP: true

# Заменить на лету 
kubectl get configmap kube-proxy -n kube-system -o yaml | \
sed -e "s/strictARP: false/strictARP: true/" | \
kubectl apply -f - -n kube-system

---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
bindAddress: 0.0.0.0
clusterCIDR: {{ pod_network_cidr }} "10.233.64.0/18"
ipvs:
  strictARP: True
mode: ipvs
---
```

#### Install 
```
# Инсталяция руками старыых версий  
# Создаем namespace metallb-system

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/namespace.yaml

# Только при первой установке создаём сикрет:

kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"

kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.10.2/manifests/metallb.yaml

# Применяем базовую конфигурацию layer2

kubectl apply -f ./mlb.yaml



#### Для инсталяции с helm (доработать values.yaml)
####  # Installation with Helm
####  helm repo add metallb https://metallb.github.io/metallb
####  # Создаем файл с именем values.yaml и вставляем шаблон:
####  # В поле addresses указываем пул IP-адресов, которые заберёт в своё пользование Metallb. 
####  # Адреса нужно указать в виде CIDR. Для одной машины  "/32".
####  configInline:
####    address-pools:
####     - name: default
####       protocol: layer2
####       addresses:
####       - 192.168.1.171/32
####  helm install metallb metallb/metallb -f values.yaml

#### Ручная установка новой версии 
#### kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.14.3/config/manifests/metallb-native.yaml
#### kubectl apply -f first-pool.yaml
#### удаление  
#### ### kubectl delete -f first-pool.yaml && rm first-pool.yaml
#### ### kubectl delete -f https://raw.githubusercontent.com/metallb/metallb/v0.14.3/config/manifests/metallb-native.yam

```
####  ingress (type loabalancer)
```
# Добавляем сервис для ingres-controller типа LoadBalancer
# на том ip который отдаст metallb на 80 443 порту будет сидеть ингрес контролеер

kubectl apply -f ./lb-ingress-controller-svc.yaml

kubectl get svc -A
NAMESPACE              NAME                                 TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)                      AGE
ingress-nginx          ingress-nginx-lb                     LoadBalancer   10.233.20.123   192.168.1.171   80:31126/TCP,443:30671/TCP   19s

http://192.168.1.171:80/
http://192.168.1.171:443/

# Также можно к любому из сервисов (с типом LoadBalancer), можно обратиться по NodePort
http://192.168.1.171:31126/


# тюнинг ingress-controler
# lb-ingress-controller-svc_upgrade.yaml
# 
# allocateLoadBalancerNodePorts: false
# решает проблему с открытием сервисов nodeport
# loadBalancerIP: 192.168.1.173
# решает проблему на каком ip запуститься
```
### Тест 
от пода с 0 (при этом был удаелен ingress (type loabalancer) созданый по выше )


kubectl create deploy nginx --image nginx

			# kubectl get all
			# NAME                         READY   STATUS    RESTARTS   AGE
			# pod/nginx-7854ff8877-fbcmj   1/1     Running   0          100s
			# 
			# NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
			# deployment.apps/nginx   1/1     1            1           101s
			# 
			# NAME                               DESIRED   CURRENT   READY   AGE
			# replicaset.apps/nginx-7854ff8877   1         1         1       101s

kubectl expose deploy nginx --port 80 --type LoadBalancer

			# kubectl get all
			# NAME                         READY   STATUS    RESTARTS   AGE
			# pod/nginx-7854ff8877-fbcmj   1/1     Running   0          10m
			# 
			# NAME                 TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
			# service/kubernetes   ClusterIP      10.233.0.1      <none>          443/TCP        84d
			# service/nginx        LoadBalancer   10.233.56.246   192.168.1.171   80:30784/TCP   4m52s
			# 
			# NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
			# deployment.apps/nginx   1/1     1            1           10m
			# 
			# NAME                               DESIRED   CURRENT   READY   AGE
			# replicaset.apps/nginx-7854ff8877   1         1         1       10m

http://192.168.1.171:80/