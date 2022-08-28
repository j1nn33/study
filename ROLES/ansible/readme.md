# описание ansible role
...
./___ansible ---/roles/___v1  # описани ролей с учетом версий
            |                    |_v2 
            |
            |__inventory_<role_name>___dev
            |                       |__prod
            |
            |_playbooks_<role_name>_back.yml  # папка с описанием playbooks
            |                     |_front.yml
            |                     |_ # например разворачиваем мониторинг (prometeus, grafana, node_exporter)
            |
            |__ansible.cfg
            |_readme.md

  # описание установки версии ansible
  # создание новой роли
  cd ./ansible/role/<role_name>
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
  ansible-playbook playbooks_monitoring/prometheus.yaml -i inventory_monitoring/dev/hosts.txt -u root --ask-pass
  ansible-playbook /root/ansible/playbooks_monitoring/prometheus.yaml -i /root/ansible/inventory_monitoring/dev/hosts.txt  --extra-vars "ansible_user=<USERNAME> ansible_password=<PASSWORD>" 
  dry run
  ansible-playbook playbooks_monitoring/prometheus.yaml -i inventory_monitoring/dev/hosts.txt --check

  --list-tasks
  --list-hosts
  --list-tags


...