Предварительная настройка хоста сразу после инсталяции

подготовка ОС
- отключение selinux     (tag: disable_selinux)
- ip v6                  (tag: disable_ip_v6)
- open vmtools           (tag: install_vmware_tools)
- отключение firewall    (tag: disable_firewall)

---------------------------
# Для быстрого тестирования 
# inventory.ini
# ansible.cfg

Запускать 
~./repo/study/ROLES/prepare_task

без ключа
ansible all -i hosts.ini -m ping -k 
с ключем
ansible.cfg   private_key_file = ~/.ssh/id_rsa
ssh-copy-id username@remote_host
ansible all -i hosts.ini -m ping -k
ansible all -i hosts.ini -m shell -a 'ps -ef | grep java'
ansible all -i hosts.ini -m command -a 'systemctl status chronyd.service'

# как запустить
ansible-playbook ./prepare_task.yml -i ./hosts.ini -k 

