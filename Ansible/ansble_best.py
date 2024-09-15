# best practice 
===========================
Установка в виртуальное окружение 
python3 -V
mkdir python-venv
cd !$

python3 -m venv ansible2.9
ls
# ansible2.9
source ansible2.9/bin/activate
(ansible2.9)$ python3 -V
# Python 3.6.8

# Установка с 0
(ansible2.9)$ python3 -m pip install ansible==2.9

# Установка из зависимостей 
# pip install -r requirements.txt || true
# pip freeze > requirements.txt

(ansible2.9)$ deactivate 


===========================
# start

ansible -i host all -m ping
ansible-inventory -i host --list

-k или --ask-pass               запросить пароль
-u <username>  или --user       
-b  или  --become
--become-user                   в какого пользователя переключисться
-K  или --ask-bekome-pass       запросить пароль для sudo
===========================
# debug
- name: playbook_for_debug
  hosts: hostname1
  vars:
    - NIFI_HOME: /tmp

# вывод переменной   
  tasks:
    - name: "task_for_debug"
      debug:
        var: NIFI_HOME

# переопределине переменной 
    - name: "set var"
      set_fact: NIFI_HOME=/tmp2
    - name: "task_for_debug"
      debug:
        var: NIFI_HOME

# получение вывода в переменную 
    - name: "Stat"
      stat:
        path: file_name
      register: stat_info
    - name: "task_for_debug"
      debug:
        var: stat_info.stat.exists


# Запуск с дебагом 
ansible-playbook -i hosts.ini playbook_name.yml -v 

ansible-playbook -i hosts.ini playbook_name.yml > output.json

# DRY RUN
ansible-playbook -i hosts.ini playbook_name.yml -C

# Примеры 
https://github.com/geerlingguy

===========================
ansible.cfg - конфигурационный файл для Ansible.

[defaults]
hostfile = ./hosts
roles = roles
remote_user = appuser
private_key_file = ~/.ssh/appuser
host_key_checking = False
===========================
Роли • Роль составляется под задачу.

Включают: tasks, handlers, variables, tests,
templates, files
$ tree db
db
├── README.md
├── defaults			Директория для переменных по умолчанию
│ └── main.yml
├── files
├── handlers			Информация о роли и зависимостях
│ └── main.yml
├── meta
│ └── main.yml
├── tasks
│ └── main.yml
├── templates
│ └── mongod.conf.j2
├── tests				Директория для тестов
│ ├── inventory
│ └── test.yml
└── vars
└── main.yml			Директория переменных, с
						большим приоритетом, чем по умолчанию
===========================
Directory layout

production                # inventory file for production servers
staging                   # inventory file for staging environment

group_vars/
   group1.yml             # here we assign variables to particular groups
   group2.yml
host_vars/
   hostname1.yml          # here we assign variables to particular systems
   hostname2.yml

library/                  # if any custom modules, put them here (optional)
module_utils/             # if any custom module_utils to support modules, put them here (optional)
filter_plugins/           # if any custom filter plugins, put them here (optional)

site.yml                  # master playbook
webservers.yml            # playbook for webserver tier
dbservers.yml             # playbook for dbserver tier

roles/
    common/               # this hierarchy represents a "role"
        tasks/            #
            main.yml      #  <-- tasks file can include smaller files if warranted
        handlers/         #
            main.yml      #  <-- handlers file
        templates/        #  <-- files for use with the template resource
            ntp.conf.j2   #  <------- templates end in .j2
        files/            #
            bar.txt       #  <-- files for use with the copy resource
            foo.sh        #  <-- script files for use with the script resource
        vars/             #
            main.yml      #  <-- variables associated with this role
        defaults/         #
            main.yml      #  <-- default lower priority variables for this role
        meta/             #
            main.yml      #  <-- role dependencies
        library/          # roles can also include custom modules
        module_utils/     # roles can also include custom module_utils
        lookup_plugins/   # or other types of plugins, like lookup in this case

    webtier/              # same kind of structure as "common" was above, done for the webtier role
    monitoring/           # ""
    fooapp/               # ""

===========================
Directory layout 2

inventories/
   production/
      hosts               # inventory file for production servers
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         hostname1.yml    # here we assign variables to particular systems
         hostname2.yml

   staging/
      hosts               # inventory file for staging environment
      group_vars/
         group1.yml       # here we assign variables to particular groups
         group2.yml
      host_vars/
         stagehost1.yml   # here we assign variables to particular systems
         stagehost2.yml

library/
module_utils/
filter_plugins/

site.yml
webservers.yml
dbservers.yml

roles/
    common/
    webtier/
    monitoring/
    fooapp/
===========================
Directory by SBER
|- Ansible
|  |__ ansible.cfg
|  |__ inventories
|  |   |__dev
|  |   |  |__APP1
|  |   |  |  |__group_vars
|  |   |  |  |  |__all.yml
|  |   |  |  |  |__secret.yml
|  |   |  |__APP2
|  |   |  |  |__group_vars
|  |   |  |  |  |__all.yml
|  |   |  |  |  |__secret.yml
|  |   |
|  |   |__prod
|  |   |  |__APP1
|  |   |  |  |__group_vars
|  |   |  |  |  |__all.yml
|  |   |  |  |  |__secret.yml
|  |   |  |__APP2
|  |   |  |  |__group_vars
|  |   |  |  |  |__all.yml
|  |   |  |  |  |__secret.yml
|  |
|  |__ playbooks
|  |   |  |__APP1
|  |   |  |  |__install.yml
|  |   |  |  |__restart.yml
|  |   |  |  |__stop.yml
|  |   |  |  |__delete.yml
|  |   |  |__APP2
|  |   |  |  |__install.yml
|  |   |  |  |__restart.yml
|  |   |  |  |__stop.yml
|  |   |  |  |__delete.yml
|  |
|  |__ roles
|  |   |  |__APP1
|  |   |  |  |__tasks
|  |   |  |     |__task_root.yml
|  |   |  |     |__task_user.yml
|  |   |  |__APP2
|  |   |  |  |__tasks
|  |   |  |     |__task_root.yml
|  |   |  |     |__task_user.yml
===========================
Тестирование Molecule, Ansible, Testinfra
requirements.txt
ansible==2.3.2
molecule==2.1.0
testinfra==1.6.3
python-vagrant==0.5.15

pip install -r requirements.txt


molecule init для создания заготовки тестов 
для роли db. Выполните команду
ниже в директории с ролью ansible/roles/db:

$ molecule init scenario --scenario-name default -r db -d vagrant

Добавим несколько тестов, используя модули Testinfra,
для проверки конфигурации, настраиваемой ролью db:
db/molecule/default/tests/test_default.py 
...
# check if MongoDB is enabled and running
def test_mongo_running_and_enabled(host):
	mongo = host.service("mongod")
	assert mongo.is_running
	assert mongo.is_enabled

# check if configuration file contains the required line
def test_config_file(File):
	config_file = File('/etc/mongod.conf')
	assert config_file.contains('bindIp: 0.0.0.0')
	assert config_file.is_file


Описание тестовой машины, которая создается Molecule
для тестов содержится в файле db/molecule/default/molecule.yml

Создадим VM для проверки роли. В директории ansible/roles/db
выполните команду:
$ molecule create

подключиться по SSH внутрь VM:
$ molecule list
Instance Name 	Driver Name Provisioner Name Created Converged
------------- ------------- ---------------- ------- -----------
instance 		Vagrant 	Ansible 		 True 	False
$ molecule login -h instance

Molecule init генерирует плейбук db/molecule/default/playbook.yml
Применим playbook.yml, в котором вызывается наша
роль к созданному хосту:
$ molecule converge


Прогоним тесты
$ molecule verify
===========================
===========================
===========================
===========================
===========================
===========================
===========================
===========================

===========================