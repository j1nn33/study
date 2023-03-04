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
ansible-playbook task_reboot.yml -i hosts.ini -e 'var_service_action=started'

----------------------------
плейбук для тестов с vault
    test_vault.yml
    environments/prod/credentials.yml
    environments/psi/credentials.yml

1. Создайте файл vault.key с паролем от файлов credentials.yml (шифровать его не надо)

2. (Опционально)
 в ansible.cfg, добавим опцию # The vault password file to use. Equivalent to –vault-password-file or –vault-id 

vault_password_file в секцию [defaults]  

3. рабочие файлы
-  ./test_vault.yml # плейбук для создания пользователей 
-  ./environments/prod/credentials.yml файл с данными пользователей для каждого окружения

4.  шифрование файлов с паролем от vault.key
ansible-vault encrypt environments/prod/credentials.yml
ansible-vault encrypt environments/psi/credentials.yml

Запуск плейбука

ansible-playbook test_vault.yml -i hosts.ini --extra-vars "inventory_dir=environments stage=prod"
ansible-playbook test_vault.yml -i hosts.ini --extra-vars "inventory_dir=environments stage=psi"

если не добаляли опцию в ansible.cfg
ansible-playbook test_vault.yml -i hosts.ini --extra-vars "inventory_dir=environments stage=psi" --vault-password-file ./vault.key
 

Для редактирования переменных нужно использовать команду
ansible-vault edit <file>

А для расшифровки: 
ansible-vault decrypt <file>

