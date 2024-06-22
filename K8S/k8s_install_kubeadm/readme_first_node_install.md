# ##############################################
# Первая control нода
# ##############################################

# описывается что делается при установке (можно проделать вручную без автоматизации) 
# После подготовки сервера readme_prepare_os.md настраиваем первую control ноду кластера.
# смотрим какие версии api поддерживает установленная версия kubeadm, который завязан на версии  

# на ноде control1.kube.local

kubeadm config print init-defaults | grep apiVersion

# apiVersion: kubeadm.k8s.io/v1beta3
# apiVersion: kubeadm.k8s.io/v1beta3

##  для следующих версий api:

InitConfiguration - kubeadm.k8s.io/v1beta3
ClusterConfiguration - kubeadm.k8s.io/v1beta3

## Для KubeProxyConfiguration и KubeletConfiguration следует использовать последнюю версию api для вашей текущей 
## версии kubernetes. Посмотреть  можно в https://kubernetes.io/docs/reference/config-api/

## control1.kube.local

mkdir /etc/kubernetes


/etc/kubernetes/kubeadm-config.yaml

```yaml
apiVersion: kubeadm.k8s.io/v1beta3
kind: InitConfiguration
bootstrapTokens:
- groups:
  - system:bootstrappers:kubeadm:default-node-token
  ttl: 24h0m0s
  usages:
  - signing
  - authentication
localAPIEndpoint:
  advertiseAddress: 192.168.1.171
  bindPort: 6443
nodeRegistration:
  criSocket: "unix:///var/run/containerd/containerd.sock"
  imagePullPolicy: IfNotPresent
  name: control1.kube.local
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
---
apiVersion: kubeadm.k8s.io/v1beta3
kind: ClusterConfiguration
certificatesDir: /etc/kubernetes/pki
clusterName: cluster.local
controllerManager: {}
dns: {}
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: "registry.k8s.io"
apiServer:
  timeoutForControlPlane: 4m0s
  extraArgs:
    authorization-mode: Node,RBAC
    bind-address: 0.0.0.0
    service-cluster-ip-range: "10.233.0.0/18"
    service-node-port-range: 30000-32767
kubernetesVersion: "v1.29.4"
controlPlaneEndpoint: 192.168.1.189:7443
networking:
  dnsDomain: cluster.local
  podSubnet: "10.233.64.0/18"
  serviceSubnet: "10.233.0.0/18"
scheduler: {}
---
apiVersion: kubeproxy.config.k8s.io/v1alpha1
kind: KubeProxyConfiguration
bindAddress: 0.0.0.0
clusterCIDR: "10.233.64.0/18"
ipvs:
  strictARP: True
mode: ipvs
---
apiVersion: kubelet.config.k8s.io/v1beta1
kind: KubeletConfiguration
clusterDNS:
#- 10.233.0.10
- 169.254.25.10   
systemReserved:
  memory: 512Mi
  cpu: 500m
  ephemeral-storage: 2Gi
# Default: "10Mi"
containerLogMaxSize: 1Mi
# Default: 5
containerLogMaxFiles: 3
```
# ############################################################################################################################
# Этот файл мы будем использовать для инициализации кластера при помощи kubeadm. 
# initConfiguration    https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta3/#kubeadm-k8s-io-v1beta3-InitConfiguration
## Основные параметры, на которые следует обратить внимание.

```yaml
bootstrapTokens:
- groups:
  ttl: 24h0m0s                                          ## по истечению 24 часов ноду не добавишь нужно выписывать новый токен
localAPIEndpoint:
  advertiseAddress: 192.168.1.171                       ## ip control1 не HA
  bindPort: 6443
nodeRegistration:
  name: control1.kube.local
  criSocket: "unix:///var/run/containerd/containerd.sock"
  imagePullPolicy: IfNotPresent
  taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
```

#  bootstrapTokens.groups[0].ttl - Время жизни токена. После инициализации первой ноды, kubeadm выведет на стандартный
#                                  вывод команды для подключения остальных нод кластера. В этих командах будет использован токен. Необходимо учесть,
#                                  что срок жизни этого токена 24 часа. Если, например через сутки, потребуется добавить новые ноды в кластер, придётся
#                                  генерировать новый токен.
#                                  bootstrapTokens.groups[0].ttl - расшифровка записи пути - секция bootstrapTokens, groups(это массив) 0-элемент массива.ttl 
#  localAPIEndpoint              - определяем IP адрес и порт, на котором на этой ноде будет слушать запросы kubernetes API сервер.
#                                  Тут надо указывать IP машины, а не кластерный IP адрес, используемый в High availability конфигурации. Если эти
#                                  параметры не указывать, kubeadm попытается автоматически определить значения. Если у вас несколько сетевых интерфесов,
#                                  лучше явно определить параметры localAPIEndpoint.  
#  nodeRegistration              - содержит поля, относящиеся к регистрации новой control ноды кластера.
#  name                          - имя хоста.
#  criSocket                     - определяем способ подключения к системе контейнеризации, установленной на ноде.
#  imagePullPolicy               - значение по умолчанию `IfNotPresent`.
#  taints                        - набор tains, устанавливаемых на ноду по умолчанию.


## ClusterConfiguration    https://kubernetes.io/docs/reference/config-api/kubeadm-config.v1beta3/#kubeadm-k8s-io-v1beta3-ClusterConfiguration
## Основные параметры, на которые следует обратить внимание.

```yaml
certificatesDir: /etc/kubernetes/pki
clusterName: cluster.local
etcd:
  local:
    dataDir: /var/lib/etcd
imageRepository: "registry.k8s.io"
apiServer:
  extraArgs:
    service-cluster-ip-range: "10.233.0.0/18"
    service-node-port-range: 30000-32767
kubernetesVersion: "v1.29.3"                 
controlPlaneEndpoint: 192.168.1.189:7443
networking:
  dnsDomain: cluster.local
  podSubnet: "10.233.64.0/18"
  serviceSubnet: "10.233.0.0/18"
```

# certificatesDir                - тут будут храниться сертификаты.
# clusterName                    - имя кластера.  
# etcd                           - определяем параметры etcd сервера. Локальный `local` сервер, установленный на control нодах. 
#                                  можно определить подключение к внешнему `external` etcd кластер.
# dataDir                        - директория, где будут находиться файлы etcd сервера.
# ImageMeta                      - параметры, при помощи которых можно указать какой контейнер использовать. Мы их явно не определяем, 
#                                  потому что `imageRepository` указан на первом уровне этого конфига. И пофакту будет использоваться он. А если явно
#                                  определить `imageTag`, то при апгрейде kubernetes на новую версию, версия контейнера etcd не изменится. 
# imageRepository                - определяем репозиторий из которого будут скачиваться образы контейнеров. Значение зависит от версии kubernetes, которую вы собираетесь использовать:
#                                  k8s.gcr.io - для 1.24
#                                  registry.k8s.io - для 1.25
#                                  свой собственный - если кластер будет устанавливаться в закрытом ИБ периметре 
# apiServer                      - дополнительный конфигурационные параметры API сервера.
#             extraArgs.service-cluster-ip-range - сеть, в которой будет выдаваться IP адреса для services кластера kubernetes.
#             extraArgs.service-node-port-range  - номера портов для сервисов типа NodePort будут барться из указанного диапазона.
# kubernetesVersion              - версия кластера kubernetes.
# controlPlaneEndpoint           - (Если используется HA то устанавливаем IP:PORT - НА ) IP адрес или DNS имя + порт. Если не определён, будут использоваться параметры из
#                                  `InitConfiguration` - `localAPIEndpoint.advertiseAddress`:`localAPIEndpoint.bindPort`. Если в кластере есть 
#                                  несколько control нод, рекомендуется указывать IP адрес внешнего балансировщика. 
# networking                     - конфигурация сети кластера.
#             dnsDomain          - имя DNS домена кластера. Значение по умолчанию `cluster.local`.
#             podSubnet          - сеть, используемая для подов кластера.
#             serviceSubnet      - сеть, используемая для сервисов кластера. Имеется в виду `kind: Service`.

## KubeProxyConfiguration    https://kubernetes.io/docs/reference/config-api/kube-proxy-config.v1alpha1/
## Создается для того чтобы использовать metalLB
## Основные параметры, на которые следует обратить внимание.

```yaml
clusterCIDR: "10.233.64.0/18"
mode: ipvs
ipvs:
  strictARP: True
```

# clusterCIDR                   - сеть, используемая для подов кластера.  
# mode                          - определяет какой механизм будет использоваться для прокси (_реализация сервисов_). Рекомендуется 
#                                 использовать `ipvs`, как самый быстрый и масштабируемый режим по сравнению с iptables.
# ipvs                          - Параметры конфигурации режима ipvs.
#             strictARP         - настраивает параметры arp_ignore и arp_announce  https://russianblogs.com/article/1259881483/  
#                                 что бы избежать ответов на запросы ARP из интерфейса `kube-ipvs0` (специальный интерфейс, используемый для работы 
#                                 сервисов, ip сервиса не может висеть в воздухе и поэтому его приземляют на kube-ipvs0). 
#                                 Для нормальной работы metallb этот парметр необходимо включить.

## KubeletConfiguration (Kubelet - приложение не под)   https://kubernetes.io/docs/reference/config-api/kubelet-config.v1beta1/
## Основные параметры, на которые следует обратить внимание.

```yaml
clusterDNS:
#- 10.233.0.10
- 169.254.25.10
systemReserved:
  memory: 512Mi
  cpu: 500m
  ephemeral-storage: 2Gi
# Default: "10Mi"
containerLogMaxSize: 1Mi
# Default: 5
containerLogMaxFiles: 3
```

# clusterDNS                   - определяем IP адреса DNS серверов кластера. Для уменьшения сетевого
#                                трафика использовать local node dns (кеширующие DNS сервера на каждой ноде кластера). Поскольку на каждой ноде будет
#                                один и тот же IP адрес, беру его из специальной сети   https://ru.wikipedia.org/wiki/Link-local_address
# systemReserved               - резервируем ресурсы для приложений работающих не под управлением kubernetes.
# containerLogMaxSize          - определяем максимальный размер файла журнала контейнера до его ротации.
# containerLogMaxFiles         - максимальный размер журнального файла контейнера.



## ############################################################################################################################
## Инициализация первой ноды

kubeadm init --config /etc/kubernetes/kubeadm-config.yaml

## Если приложение долго не завершает свою работу, значит что-то пошло не так. Необходимо отменить все действия и запустить
## его ещё раз, но с большим уровнем отладки.

kubeadm reset
kubeadm init --config /etc/kubernetes/kubeadm-config.yaml -v5

## Если и там не видно смотрим логи kubelet /var/log/messages
##  Если нода установилась нормально, добавим конфиг kubectl. И посмотрим, всё ли действительно у нас нормально.

mkdir -p $HOME/.kube
ln -s /etc/kubernetes/admin.conf $HOME/.kube/config

##  cделать символьную ссылку. Но можно файл скопировать.
##  посмотрите какой IP адрес анонсирует кластер для доступа к своему API:

kubectl cluster-info

##  Убедимся, что нода в кластере.

kubectl get nodes

##  Убедимся, что на самом деле ничего не работает.

watch kubectl get pods -A

## Потому что у нас не работает DNS и внутренняя сеть кластера.
##  Добавим удобства в работе с kubectl, автодополнение. _Данная фишка будет работать только с bash._

source <(kubectl completion bash)
echo "source <(kubectl completion bash)" >> ~/.bashrc

## nodelocaldns

## Для нормальной работы нам необходимо установить кеширующий DNS сервер.
## Сначала узнаем IP адрес основного DNS сервера кластера. Он нам понадобится на следующем шаге. 


kubectl -n kube-system get svc kube-dns -o jsonpath='{.spec.clusterIP}'


## Подставим его в фале манифеста  /etc/kubernetes/nodelocaldns-daemonset.yaml на 24-й, 36-й и 47-й строках. или K8S/ansible/roles/master/templates/nodelocaldns-daemonset.j2

## Мы определяем куда будут пересылаться запросы о соответствующих зонах. При запросе к основному
## DNS серверу наш сервер переходит на tcp, хотя обычно для этого используется udp трафик. 
## Udp не устанавливает соединение и, соответственно не может его закрыть. Количество соединений в таблице ip_conntrack 
## ограничено, и в принципе возможно ее переполнение. Ну и с nat преобразованиями у udp бывают проблемы. Не использовать udp в kubernetes.
## На 58-й строке мы говорим, что запросы ко всем остальным доменам будут пересылаться на DNS сервера, указанные
## в файле /etc/resolve.conf сервера Linux. Если бы у нас не было кеширующего сервера, то все запросы сначала шли внутри 
## сети кубера на основной DNS сервера, а потом уходили на внешние серевера DNS. Немного трафика внутри кубера сэкономили.   
## 
## Скопируем файл манифеста на первую ноду кластера в  `/etc/kubernetes/nodelocaldns-daemonset.yaml`. И запустим приложение.

kubectl apply -f /etc/kubernetes/nodelocaldns-daemonset.yaml

## Обратите внимание на 23-ю строку: `hostNetwork: true`. Это значит что контейнер будет открывать порт на прослушивание на сетевых интерфейсах хоста.

ss -nltp | grep :53

## Поскольку мы использовали DaemonSet, кеширующий DNS сервер будет автоматически запускаться на всех нодах кластера. 

## CNI plugin (Драйвер сети) 
#    https://www.tigera.io/tigera-products/calico/  
#    https://docs.tigera.io/archive

## calico. список драйверов    https://github.com/containernetworking/cni#3rd-party-plugins
## Будем ставить при помощи оператора. Сначала сам опреатор:

kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.24.5/manifests/tigera-operator.yaml

# Пока в системе устанавливаются CRD calico. необходимо время для применения манифеста на ноде 
# манифест для оператора  /etc/kubernetes/calico-install.yaml или K8S/ansible/roles/master/templates/calico-install.j2

# В 14-й и 15-й строках укажите параметры вашей сети.
# cidr                      - сеть, используемую для подов кластера. (_Сетью для сервисов будет управлять kube-proxy_)
# encapsulation             - режим энкапсуляции трафика. Возможные варианты: IPIP, VXLAN, IPIPCrossSubnet, VXLANCrossSubnet, None.
#                             IPIP или IPIPCrossSubnet. Несмотря на то, что это энкапсуляция IP в IP, а не Ethernet в
#                             в IP (вариант VXLAN*). C VXLAN могут быть сюрпризы.

## Скопируйте файл в `/etc/kubernetes/calico-install.yaml`. И примените манифест.

kubectl apply -f /etc/kubernetes/calico-install.yaml

# Проверяем, что все поды запустились.


watch kubectl get pods -A

# ####################################################
# Автоматизация

# tooks@ubuntubastion:~/K8S/ansible/$ 
ansible-playbook services/install-1st-control.yaml

##  посмотрите какой IP адрес анонсирует кластер для доступа к своему API:

kubectl cluster-info

##  Убедимся, что нода в кластере.

kubectl get nodes
kubectl get pods -A

#  поды CoreDNS не запускались на первой ноде 
kube-system        coredns-6                      0/1     Pending

# Дело 
kubectl describe node control1.kube.local | grep Taints
# Taints:             node-role.kubernetes.io/master:NoSchedule
kubectl describe pod <name_pod> -n kube-system

# решение убрать и возратить 
kubectl taint nodes control1.kube.local node-role.kubernetes.io/master-

kubectl taint nodes control1.kube.local node-role.kubernetes.io/master:NoSchedule
