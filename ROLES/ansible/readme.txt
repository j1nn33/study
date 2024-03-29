# описание ansible role
...
./___ansible ---/roles/___v1  # описани ролей с учетом версий
            |                    |_v2 
            |
            |__inventory_<role_name>___dev
            |                       |__prod
            |
            |_playbooks_<role_name>_back.yml  # папка с описанием playbooks
            |                     |_front_role.yml
            |                     |_ # например разворачиваем мониторинг (prometeus_role, grafana_role, node_exporter_role)
            |                     |_ # окончание _role обязательно  
            |
            |_roles_______________
            |                     |_<role_name>  # собраны таски запуска роли
            |                     |_test_playbook   
            |
            |__ansible.cfg
            |_readme.md

Описание структуры версии 2 

./___ansible ---/roles/

├── ansible.cfg
├── inventory_<role_name> -
|            |-PROD├── group_vars  
│                  ├── all.yml
│                  ├── group1.yml
│                  └── group2.yml
├                  ├── host_vars
│                  ├── sever1
│                  ├── sever2
│                  
|            |-DEV ├── group_vars  
│                  ├── all.yml
│                  ├── group1.yml
│                  └── group2.yml
├                   ── host_vars
│                  ├── sever1
│                  ├── sever2
│                 
|_playbooks_<role_name>_back.yml  # папка с описанием playbooks
|                     |_front_role.yml
|                     |_ # например разворачиваем мониторинг (prometeus_role, grafana_role, node_exporter_role)
|                     |_ # окончание _role обязательно  
|
├── group_vars  
│   ├── all.yml
│   ├── group1.yml
│   └── group2.yml
├── host_vars
│   ├── sever1
│   ├── sever2
│  
|
└── roles
    ├── <role_name>  # собраны таски запуска роли
    │   ├── files
    │   ├── templates
    │   ├── tasks
    │   ├── handlers
    │   ├── vars
    │   ├── defaults
    │   └── meta
    └── test_playbook
readme.md     

  # описание установки версии ansible
  # создание новой роли c именем v1
  относительно каталога study  
  cd ./ROLES/ansible/role/
  mkdir <role_name>
  cd ./ROLES/ansible/role/<role_name>

  ansible-galaxy init <v1>
  ...
  defaults — переменные по умолчанию. У них самый низкий приоритет и их могут легко переопределить переменные в каталоге vars (ниже по списку).
  files — для файлов, которые могут быть скопированы на настраиваемый сервер.
  handlers — обработчики, которые могут запускаться при определенных обстоятельствах. Например, перезапуск сервиса в случае обновления конфигурационного файла.
  meta — добавление метаданных, например: автор, описание, среда и так далее.
  tasks — папка с описанием выполняемых задач.
  templates — файлы с шаблонами. Мы можем использовать переменные в данных шаблонах — тогда при копировании файлов, они будут заменяться значениями.
  tests — скрипты для выполнения тестов — ansible покажет результаты выполнения команд, но не применит их.
  vars — файлы с переменными. Имеют высокий приоритет.
  ...
  # запуск команд
  
  ansible-playbook playbooks_<role_name>/back.yml -i inventory_<role_name>/dev
  
  ansible-playbook playbooks_monitoring/prometheus.yaml -i inventory_monitoring/dev/hosts.txt   
  ansible-playbook playbooks_monitoring/prometheus.yaml -i inventory_monitoring/dev/hosts.txt --ask-become-pass 
  # Failed to connect to the host via ssh: Permission denied (publickey,password)
  #ansible-playbook playbooks_monitoring/prometheus.yaml -i inventory_monitoring/dev/hosts.txt -u root --ask-pass
  
  # запуск для конкретного репозитория 
  cd ./root/repo/study
  ansible-playbook ./ROLES/ansible/playbooks_monitoring/prometheus_role.yaml -i ./ROLES/ansible/inventory_monitoring/dev/hosts.ini 
  
  #ansible-playbook /root/ansible/playbooks_monitoring/prometheus.yaml -i /root/ansible/inventory_monitoring/dev/hosts.txt  --extra-vars "ansible_user=<USERNAME> ansible_password=<PASSWORD>" 
  dry run
  #nsible-playbook playbooks_monitoring/prometheus.yaml -i inventory_monitoring/dev/hosts.txt --check
   
  --list-tasks
  --list-hosts
  --list-tags


...
Jenkins
---------------------
#  описание pipeline jenkins для запуска тестового (пароли не требуются)

pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('git') { // download from git
            steps {
                git branch: 'master', url: "https://github.com/j1nn33/study.git" // используем встроенный в Jenkins плагин Git для скачивания проекта из бранча main
            }
        }
        
        stage('execute Ansible') {
            steps {
                ansiblePlaybook colorized: true, disableHostKeyChecking: true, installation: 'ansible-master', inventory: './ROLES/ansible/roles/test_playbook/inventory.ini', playbook: './ROLES/ansible/roles/test_playbook/test_playbook.yaml'   
            }    
        }
    }    
}


---------------------
#  описание pipeline jenkins для запуска prometeus (пароли зашиты в кредах jenkins)
pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('git') { // download from git
            steps {
                git branch: 'master', url: "https://github.com/j1nn33/study.git" // используем встроенный в Jenkins плагин Git для скачивания проекта из бранча main
            }
        }
        
        stage('execute Ansible') {
            steps {
                ansiblePlaybook become: true, colorized: true, credentialsId: 'ssh_cred_for_host', disableHostKeyChecking: true, installation: 'ansible-master', inventory: './ROLES/ansible/inventory_monitoring/dev/hosts.ini', playbook: './ROLES/ansible/playbooks_monitoring/prometheus_role.yaml'
            }    
        }
    }    
}

---------------------
#  описание pipeline jenkins для запуска grafana (пароли зашиты в кредах jenkins)
pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('git') { // download from git
            steps {
                git branch: 'master', url: "https://github.com/j1nn33/study.git" // используем встроенный в Jenkins плагин Git для скачивания проекта из бранча main
            }
        }
        
        stage('execute Ansible') {
            steps {
                ansiblePlaybook become: true, colorized: true, credentialsId: 'ssh_cred_for_host', disableHostKeyChecking: true, installation: 'ansible-master', inventory: './ROLES/ansible/inventory_monitoring/dev/hosts.ini', playbook: './ROLES/ansible/playbooks_monitoring/grafana_role.yaml'
            }    
        }
    }    
}
---------
#  описание pipeline jenkins для запуска nodeexporter (пароли зашиты в кредах jenkins)

pipeline {  
  agent {
        label 'master'
    }
    stages {
        stage('git') { // download from git
            steps {
                git branch: 'master', url: "https://github.com/j1nn33/study.git" // используем встроенный в Jenkins плагин Git для скачивания проекта из бранча main
            }
        }
        
        stage('execute Ansible') {
            steps {
                ansiblePlaybook become: true, colorized: true, credentialsId: 'ssh_cred_for_host', disableHostKeyChecking: true, installation: 'ansible-master', inventory: './ROLES/ansible/inventory_monitoring/dev/hosts.ini', playbook: './ROLES/ansible/playbooks_monitoring/node_exporter_role.yaml'
            }    
        }
   }
}