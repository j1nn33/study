# Установка кластера 
  K8S/k8s_install_kubeadm

# Архитектура стенда              - readme_stand.md
# установка python3               - /services/install_python3.yaml
# Предварительная настройка ОС    - readme_prepare_os.md
# High availability               - readme_ha.md
# Установка кластера              - readme_kubeadm_install.md
# ansible                         - автоматизация K8S/ansible/README.md
# Установка первой ноды           - readme_first_node_install.md
# Добавление control nodes        - readme_add_other_control_node.md
# Добавление worker ноды          - readme_worker-nodes.md
# Проверка работоспособности      - readme_check.md
# Выключение кластера             - /services/poweroff.yaml
# Удаление кластера               - /services/reset.yaml
# Обновление версии кластера      - readme_update.md
# Удаление нод                    - readme_delete_node.md
# Обновление сертификатов         - readme_certificates.md


# ============================ #
# ansible  
  # для kubeadm
  - kubeadm 
    - K8S/ansible/kubeadm/group_vars/k8s_cluster    - список переменных
    - K8S/ansible/kubeadm/hosts.yaml                - inventory


# ###################################################
####                      ЧАСТИЧНАЯ АВТОМАТИЗАЦИЯ  
# ###################################################
         
cd K8S/ansible

# - Предварительная настройка ОС                                
ansible-playbook services/prepare-hosts.yaml

# - Установка первой ноды 
ansible-playbook services/install-1st-control.yaml

# - Добавление node в cluster
# - добавление дополнительной control-node
ansible-playbook services/install-another-controls.yaml

# - добавление дополнительной worker-node
ansible-playbook services/install-workers.yaml

# ###################################################
####                      ПОЛНАЯ АВТОМАТИЗАЦИЯ  
# ###################################################


## Установка для KUBEADM

### k8s с одной control node
# В K8S/ansible/kubeadm/hosts.yaml в группе `k8s_masters` необходимо указать только один хост.

ansible-playbook install-cluster.yaml


### k8s с несколькими control nodes
# В K8S/ansible/kubeadm/hosts.yaml в группе `k8s_masters` необходимо указать нечётное количество control nodes.

ansible-playbook install-cluster.yaml

### k8s c HA
# Используются haproxy и keepalived.
# В конфигурационном файле определите параметры доступа к API :
#                `ha_cluster_virtual_ip` - виртуальный IP адрес.
#                `ha_cluster_virtual_port` - порт. Не должен быть равен 6443.

## Удалить кластер Скрипт удаляет **все** нестандартные цепочки и чистит все стандартные цепочки.

ansible-playbook reset.yaml

## Апдейт кластера
# Изменяете версию кластера в `group_vars\k8s_cluster` и запускаете апдейт.

ansible-playbook upgrade.yaml

## Сервисные функции находятся в директории `services`