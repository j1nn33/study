# Для быстрого тестирования 
# inventory.ini
# ansible.cfg

Запускать 
~./repo/study/ROLES/test_task

без ключа
ansible all -i hosts.ini -m ping -k --ask-become-pass

с ключем
ansible.cfg   private_key_file = ~/.ssh/id_rsa

 ssh-copy-id username@remote_host

ansible all -i hosts.ini -m ping
ansible all -i hosts.ini -m shell -a 'ps -ef | grep java'
ansible all -i hosts.ini -m command -a 'systemctl status chronyd.service'



https://github.com/j1nn33/study/blob/master/Ansible/ansible_IDV-IT.txt

ansible-playbook test_task.yml -i hosts.ini 

