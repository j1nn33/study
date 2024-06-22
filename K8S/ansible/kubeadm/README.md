# Ansible playbook для установки кластера k8s поддерживает:

# Установку одной или несколько control nodes.
# HA доступ к API kubernetes.
# containerd.
# calico.
# В KubeProxyConfiguration установлены параметры для работы Metallb.
# nodelocaldns - кеширующий DNS сервер на каждой ноде кластера.


##      -     УСТАНОВКА ПОЛУАВТОМИТИЧЕСКАЯ
##      -     УСТАНОВК АВТОМАТИЧЕСКАЯ k8s с одной control node
##      -     УСТАНОВК АВТОМАТИЧЕСКАЯ k8s с несколькими control nodes 
##      -     УСТАНОВК АВТОМАТИЧЕСКАЯ с HA Используются haproxy и keepalived
##      -     Удалить кластер Скрипт удаляет **все** нестандартные цепочки и чистит все стандартные цепочки.
##      -     Апдейт кластера


# Установка ansible Ubuntu 

apt install python3.10-venv
python3 -m venv venv
. ~/venv/bin/activate
python3 -m pip install ansible

# Генерируем ssh ключ:

ssh-keygen

# Копируем ключики в виртуальные машины из K8S/ansible/kubeadm/hosts.yaml:

ssh-copy-id root@control1.kube.local
ssh-copy-id root@control2.kube.local
ssh-copy-id root@control3.kube.local
ssh-copy-id root@worker1.kube.local
ssh-copy-id root@worker2.kube.local
ssh-copy-id root@worker3.kube.local
ssh-copy-id root@db1.kube.local

## Конфигурационные параметры и структура

- K8S/ansible/group_vars/k8s_cluster    - список переменных
- K8S/ansible/hosts.yaml                - inventory
- K8S/ansible/services                  - папка с описанием вызова ролей 
- K8S/ansible/roles                     - описание ролей 
# --------------
# Проверка  
ansible-playbook services/ping.yaml
ansible all -i hosts.yaml -m shell -a 'date'

# --------------

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



# ###########################################################
## Установка 
### k8s с одной control node
# В K8S/ansible/hosts.yaml в группе `k8s_masters` необходимо указать только один хост.

ansible-playbook install-cluster.yaml

### k8s с несколькими control nodes
# В K8S/ansible/hosts.yaml в группе `k8s_masters` необходимо указать нечётное количество control nodes.

ansible-playbook install-cluster.yaml

### k8s c HA Используются haproxy и keepalived. images/ha_cluster.jpg
# В конфигурационном файле определите параметры доступа к API :
#  `ha_cluster_virtual_ip` - виртуальный IP адрес.
#  `ha_cluster_virtual_port` - порт. Не должен быть равен 6443.

## Удалить кластер Скрипт удаляет **все** нестандартные цепочки и чистит все стандартные цепочки.

ansible-playbook reset.yaml

## Апдейт кластера
# Изменяете версию кластера в `group_vars\k8s_cluster` и запускаете апдейт.

ansible-playbook upgrade.yaml

## Сервисные функции находятся в директории `services`