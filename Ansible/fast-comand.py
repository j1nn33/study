ansible
short command

dir/
   ansible.cfg
   hosts.txt

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
