ansible
short command

dir/
   ansible.cfg
   hosts.txt



============
ansible -i <name_inventory_file> all -m shell -a '<bash_command>'
ansible -i <name_inventory_file> all -m shell -a '<bash_command>' -b

time ansible -i <name_inventory_file> all -m shell -a '<bash_command>'

ansible -i <name_inventory_file> all -m  -k shell -a '<bash_command>' 

ansible-playbook <name>.yaml -i <inventory> --check
ansible-playbook <name>.yaml -i <inventory> --ask-pass
ansible-playbook <name>.yaml -i <inventory> -u <user> --private-key file.txt

============ VAULT
cat <name_keytab> | base64 > <name_file>

ansible-vault encrypt <name_file>
ansible-vault decrypt <name_file>

# расшифровка паролем записанным в файл name_file_pass
ansible-vault decrypt <name_file> --vault-password-file=<name_file_pass>

# зашифровать отдельную строку

ansible-vault encrypt_string --vault-id @promt <my_password>
============




-------------------------
host_key_checking = false
inventory = ./inventory/hosts.txt
#become: yes
-------------------------
[all]
192.168.1.103

-------------------------   
ansible all -a "systemctl status nginx"

ansible all -a "systemctl status nginx & systemctl status firewalld" 

ansible all -m setup | grep -A2 -B2 ipv4

ansible all -m ping -u <username>

ansible all -m ping -u <username> --ask-pass

ansible all  -a 'free -h'

----------------------------
YAML

lists:
  - item1
  - item2

dict:
  key1: val1
  key2: 'val2'
