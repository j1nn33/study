# роли независимые доступные для перемещения

ansible-galaxy init <role_name>

------------------------------
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
  cd <role_name_dir>
  ansible-playbook playbooks_<role_name>.yml -i ./inventory/dev
  
  ansible-playbook ipa_security.yaml -i ./invenory/dev/ -k -b 

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
   
 -------------------------

