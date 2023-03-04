# Для быстрого тестирования 
# https://github.com/teamclairvoyant/hadoop-smoke-tests/blob/master/Cloudera-CDH.md
# inventory.ini
# ansible.cfg

Запускать 
~./repo/study/ROLES/test_task

без ключа
ansible all -i hosts.ini -m ping -k 

с ключем
ansible.cfg   private_key_file = ~/.ssh/id_rsa

ssh-copy-id username@remote_host

ansible all -i hosts.ini -m ping -k


ansible all -i hosts.ini -m shell -a 'ps -ef | grep java'
ansible all -i hosts.ini -m command -a 'systemctl status chronyd.service'

ansible-playbook ./test_task.yml -i ./hosts.ini -k 



