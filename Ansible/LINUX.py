Ansible

Control machine 	— управляющий хост. Сервер Ansible, с которого происходит
					  управление другими хостами
Manage node 		— управляемые хосты 
Inventory 			— инвентарный файл. В этом файле описываются хосты, группы хостов,
					  а также могут быть созданы переменные
Playbook		    — файл сценариев
Play 				— сценарий (набор задач). Связывает задачи с хостами, для которых эти
					  задачи надо выполнить
Task				— задача. Вызывает модуль с указанными параметрами и переменными
Module 				— модуль Ansible. Реализует определенные функции
===================================================================================


 Ansible - Установка на Ubuntu 16.04 и CentOS 7


Установка на Ubuntu 16.04:
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible

Установка на CentOS 7:
sudo yum install epel-release
sudo yum install ansible

---------------------------------
ansible --version
---------------------------------
настройка

./ansible.cfg – в текущем каталоге;
~/.ansible.cfg — в домашнем каталоге;
/etc/ansible/ansible.cfg 

---------------------------------

hostfile: — путь к inventory file, содержит список ip-адресов (или имен) хостов для подключения;
library: — путь к модулям Ansible;
forks: — кол-во потоков, которые может создать Ansible;
sudo_user: — пользователь, от которого запускаются команды/инструкции на удаленных хостах;
remote_port: — порт для подключения по протоколу SSH;
host_key_checking: — включить/отключить проверку SSH–ключа на удаленном хосте;
timeout: — таймаут подключения по SSH;
log_path: — путь к файлу логов.

----------------------------------
Генерация SSH-ключа на сервере ansible

ssh-keygen -C "$(whoami)@$(hostname)-$(date -I)"

Если при генерации ключа на все вопросы был дан стандартный ответ (клавишей Enter), 
то в каталоге ~/.ssh/ появится два файла — id_rsa (закрытый ключ) и id_rsa.pub (открытый ключ).

Открытый ключ нужно скопировать на удаленный сервер, 
это можно сделать с помощью команды ssh-copy-id, например так:
ssh-copy-id user@server     

user - пользователь на удаленном сервере

Еще один способ скопировать открытый ключ на удаленный сервер — скопировать содержимое
~/.ssh/id_rsa.pub с локального компьютера в файл ~/.ssh/authorized_keys на удаленном хосте. 
Важно: чтение/запись в этот файл может производить только владелец, добиться этого можно командой:
chmod 600 ~/.ssh/authorized_keys


===================================================================================

структра проекта 
в корневой папке /etc/root/ansible
-rw-r--r-- 1 root root 19315 May 12 10:30 ansible.cfg
-rw-r--r-- 1 root root   251 May 12 10:32 hosts
-rw-r--r-- 1 root root   116 May 12 10:26 playbook1.yml


-----------------------------------------------------------------------------------
ansible.cfg

[defaults]

inventory      = /root/ansible/hosts

host_key_checking = False

[privilege_escalation]
become=True
become_method=sudo
become_user=root
become_ask_pass=False

===================================================================================
Inventory 
------------------------1 вариант   CISCO-------------------------
[cisco-routers]  		# название группы
192.168.255.1:22022     # использование не стандартного порта ssh
192.168.255.2

[cisco-edge-routers]
192.168.255.1			# oдин и тот же адрес или имя хоста можно помещать в разные группы
92.168.255.[1-5]

[cisco-devices:children] # группа из групп
[cisco-edge-routers]
[cisco-routers] 

------------------------2 вариант-------------------------
/etc/ansible/hosts
[instance]
192.168.10.201                                                  # centos
192.168.10.202 ansible_user=tooks ansible_sudo_pass=Aa123456    # ubuntu

-----------------проверить 2 вариант----------------------

ansible instance -m ping

===================================================================================
Ad-hoc команды - это возможность запустить какое-то действие Ansible из командной строки.
-------------------------------------------
ansible-inventory  --list
ansible-inventory  --graph

ansible 192.168.10.202 -m setup
ansible all -m shell -a "uptime"
#  all     - все компы
# -m       - модуль (команда ansible)
# shell    - запуск на удаленном хосте shell
# -a       - аргумент который передается shell
# "uptime" - команда выполняемая в shell

===================================================================================
Переменные
можно создавать словари с переменными (в формате YAML):
R1:
  IP: 10.1.1.1/24
  DG: 10.1.1.100
Обращаться к переменным в словаре можно двумя вариантами:
R1['IP'] - предпочтительнее
R1.IP    - могут быть проблемы если название ключа совпадает с зарезервированным словом

===================================================================================
----------------------------------

о правилах написания YAML-файлов:
все YAML-файлы должны начинаться с "---". Эта часть формата YAML означает начало документа;
члены списка должны начинаться с пробела или "-" и иметь одинаковые отступы от начала строки;
комментарии начинаются с символа "#";
словарь описывается в виде «ключ» ": " «значение» и может быть представлен в сокращенной форме.

----------------------------------
Узнать, на каких хостах будет происходить работа, можно командой:

ansible-playbook <имя_набора_инструкций> --list-host
----------------------------------

PLAYBOOK
#-----1
---
- name: Test Connection to my servers
  hosts: all
  become: yes

  tasks:

  - name: Ping my servers
    ping:
#
ansible-playbook playbook.yml


#------2----Centos
---
- name: Install default Apsche WEB
  hosts: all
  become: yes

  tasks:
  - name: Install Apache Webserver
    yum: name=httpd state=latest

  - name: Start Apache and Enable it on thr every boot
    service: name=httpd state=started enabled=yes
#------3----Ubuntu
---
- hosts: test
  tasks:

  - name: Install package nginx
    apt: name=nginx update_cache=yes
    sudo: yes

  - name: Starting service nginx
    service: name=nginx state=started
    sudo: yes

#-------4-----UNUVERSAL
---
- name: Install Apache Webserver
  hosts: all
  become: yes
  tasks:
 
  - name: Debug
    debug: msg={{ ansible_os_family }}
 
  - set_fact: package_name=httpd
    when: ansible_os_family == "Redhat"
 
  - set_fact: package_name=apache2
    when: ansible_os_family == "Debian"
 
  - name: Install httpd package
    yum: name={{ package_name }} state=latest
    sudo: yes
    when: ansible_os_family == "Redhat"
  
  - name: Install apache2 package
    apt: name={{ package_name }} state=latest
    sudo: yes
    when: ansible_os_family == "Debian"

#-------5-------
# playbook станавливает apache и заливает файл если изменить файл и запустить playbook
# снова то система поймет что файл изменилс и перезапустит apache
# если файл не измениться то apace не будет перезапускаться
---
- name: Install Apache and Upload Webpage, when Webpage is change Apache will be restart
  hosts: all
  become: yes

  vars:
    source_file: ./MyWebSite/index.html
    destin_file: /var/www/html

  tasks:
  - name: Install Apache Webserver
    yum: name=httpd state=latest

  - name: Copy MyWebSite page 
    copy: src={{ source_file }} dest={{ destin_file }} mode=0555
    notify: Restart Apache

  - name: Start Webserver and make it enabled on boot
    service: name=httpd state=started enabled=yes

  handlers:
  - name: Restart Apache
  service: name=httpd state=restart

  #---------------------------
===================================================================================
