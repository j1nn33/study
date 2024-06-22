# Предварительные действия. (описание ручной установки )
# На всех машинах, где будет установлен кластер kubernetes, необходимо:
# 1 -  Отключить swap.
# 2 - Отключить firewall.
# 3 - Отключить selinux.        (можно не отключать)
# 4 - Настроить параметры ядра.
# 5 - Установить приложения.


## 1 Отключить swap
# В файле `/etc/fstab` закоментируйте строку, определяющую подключение swap пространства.

swapoff -a


## 2 Отключить firewall

systemctl stop firewalld
systemctl disable firewalld

# Убедитесь, что в фаерволе нет правил и установлены политики по умолчанию ACCEPT:

iptables -L -n
iptables -t nat -L -n
iptables -t mangle -L -n
iptables -t raw -L -n 


## 3 Отключить selinux
# В файле `/etc/selinux/config` установите значение переменной `SELINUX` в `disabled` или, если в дальнейшем захотите настроить правила selinux, в `permissive`.

setenforce 0
sudo sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

## 4 Настроить параметры ядра
# Сначала загрузите модуль `br_netfilter`:

modprobe br_netfilter

#  для загрузки модуля при старте системы добавьте файл `/etc/modules-load.d/modules-kubernetes.conf`:  

br_netfilter

# В файл `/etc/sysctl.conf` добавтье следующие строки:

net.ipv4.ip_forward=1
net.bridge.bridge-nf-call-iptables=1
net.bridge.bridge-nf-call-ip6tables=1
net.ipv4.ip_nonlocal_bind=1

# Load settings from all system configuration files
sysctl --system

# ---------------ПРОВЕРКА 

lsmod | grep br_netfilter
# br_netfilter           24576  0
# bridge                188416  1 br_netfilter

sysctl -a | grep net.bridge.bridge-nf-call

# ---------------
## 5 Установить приложения.

# Добавляем репозиторий kubernetes. Для этого создаём файл `/etc/yum.repos.d/kubernetes.repo`:
# См актуальный файл в автоматизации  https://v1-29.docs.kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/


cat <<EOF | sudo tee /etc/yum.repos.d/kubernetes.repo
[kubernetes]
name=Kubernetes
baseurl=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/
enabled=1
gpgcheck=1
gpgkey=https://pkgs.k8s.io/core:/stable:/v1.29/rpm/repodata/repomd.xml.key
exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni
EOF

# Обязательные:

dnf install -y bash-completion python3 tar containerd nfs-utils chrony
yum install -y kubelet kubeadm kubectl --disableexcludes=kubernetes

# Не обязательные:

dnf install -y mc vim git rsyslog jq

## Запуск необходимых сервисов

### NTP

systemctl enable chronyd
systemctl start chronyd
systemctl status chronyd

### syslog Опционально включаем систему логирования rsyslog

systemctl enable rsyslog
systemctl start rsyslog
systemctl status rsyslog


### Система контейнеризации containerd.

systemctl enable containerd
systemctl start containerd
systemctl status containerd

# Добавим конфигурационный файл `/etc/crictl.yaml` для приложения управления контейнерами  https://github.com/kubernetes-sigs/cri-tools/blob/master/docs/crictl.md

runtime-endpoint: "unix:///run/containerd/containerd.sock"
image-endpoint: "unix:///run/containerd/containerd.sock"
timeout: 0
debug: false
pull-image-on-create: false
disable-pull-on-run: false

# Проверим работоспособность утилиты:

crictl images
crictl ps -a


# Проверка 

ansible all -i hosts.yaml -m shell -a 'crictl -v'
ansible all -i hosts.yaml -m shell -a 'systemctl status containerd.service | grep Active'
ansible all -i hosts.yaml -m shell -a 'kubectl version'


ansible all -i hosts.yaml -m shell -a 'lsmod | grep br_netfilter'

## br_netfilter           36864  0
## bridge                409600  1 br_netfilter

ansible all -i hosts.yaml -m shell -a 'lsmod | grep overlay'

## overlay               233472  0
 
ansible all -i hosts.yaml -m shell -a 'sysctl net.bridge.bridge-nf-call-iptables net.bridge.bridge-nf-call-ip6tables net.ipv4.ip_forward'

## net.bridge.bridge-nf-call-iptables = 1
## net.bridge.bridge-nf-call-ip6tables = 1
## net.ipv4.ip_forward = 1

ansible all -i hosts.yaml -m shell -a 'swapon -s'

##  Ожидаемый вывод команды – пустой. Она ничего не должна отобразить.
