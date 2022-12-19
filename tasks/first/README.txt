------------------------------------
описание  first
1:
  - поднять базу postgresql
  - сделать скрипт мониторинга CPU, RAM, SWAP
  - скрипт поставить на расписание
  - таблица в БД (дата и результаты скрипта)
  - запрос как посмотреть за это время
  - nginx (страница которая выводит результаты из БД за это время)

2: 

------------------------------------
# Для быстрого тестирования 
# inventory.ini
# ansible.cfg

Запускать 
~./repo/study/task/first/infra

без ключа
ansible all -i hosts.ini -m ping -k --ask-become-pass

с ключем
ansible.cfg   private_key_file = ~/.ssh/id_rsa

 ssh-copy-id username@remote_host

ansible all -i hosts.ini -m ping
ansible all -i hosts.ini -m command -a 'systemctl status chronyd.service'

--------------------------------------
развертывание postgreSQL

ansible-playbook setup_postgreSQL.yml -i hosts.ini

Тестирование инсталяции

su - postgres
psql
получение списка таблиц
\dt *
\q


