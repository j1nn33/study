BEST PRACTICE
==========================================
очередь

- name: installing zsh
  apt: pkg=$item
  with_items:
    - zsh
    - htop
    - sudo
    - iftop
    - tcpdump
    - mc

==========================================
Добавление пользователей 

- name: Add User Pupkin
  user: name='pupkin' shell='/bin/zsh' groups='sudo'

или

- name: Add BestAdminsTeam
  user: name={{ item.user }} shell={{ item.shell }} groups='sudo'
  with_items:
    - { user: 'pupkin', shell: '/bin/zsh' }
    - { user: 'oldfag', shell: '/bin/sh' }

==========================================
2 - вариант
 
 ./roles/main/variables/main.yml в который запишем: 

ssh_super_team:
    - { user: 'pupkin', key: 'ssh-rsa pupkin_pub_key', shell: '/bin/zsh'}
    - { user: 'oldfag', key: 'ssh-rsa oldfag_pub_key', shell: '/bin/sh' }


Теперь в задаче можем использовать переменную $ssh_super_team вот так: 

- name: Add BestAdminsTeam
  user: name={{ item.user }} shell={{ item.shell }} groups='sudo'
  with_items:
    - $ssh_super_team

- name: Add BestAdminsKey
  authorized_key: user={{ item.user }} key="{{item.key}}"
  with_items:
    - $ssh_super_team


Ну и чтобы сделать всем удобно — скопируем нашим пользователям файл .vimrc — одинаковый для обоих пользователей.
В каталог ./roles/main/files/ сунем файл по имени ‘vimrc’ и сделаем такой таск: 

- name: copy vimrc file
  copy: src="\vimrc" dest="/home/{{item.user}}/.vimrc"
  with_items:
    - $ssh_super_team

==========================================
ansible_sudo_pass можно переопределять в нескольких местах:
для каждого отдельного хоста в инвентарном файле                        inventory/inventoryname/hosts
для группы хостов в инвентарном файле                                   inventory/inventoryname/groups (как раз наш случай)
для группы хостов в файле групповых переменных                          group_vars/groupname/ansible.yml
для группы хостов в файле групповых переменных в зашифрованном виде     ansible-vault create group_vars/groupname/ansible.yml

«безопасности» - зашифрованный пароль, то следует использовать ansible-vault. 

Сначала создадим файл, в котором будет храниться пароль для получения привилегий суперпользователя:
# ansible-vault create secret

В созданный файл secret следует добавить строку вида:

ansible_sudo_pass: VeryStrongPassword

И, так как мы все равно не хотим вводить пароль при запуске плейбука (даже пароль ansible-vault), 
то создадим файл vault.txt (не забываем выставит корректные права доступа):
# touch vault.txt

В котором в текстовом виде запишем свой пароль от ansible-vault.

Далее приводим playbook к примерно такому виду:

---
- hosts: all
  become: yes
 
  vars_files:
    - secret
 
  tasks:
  - name: Add user to remote hosts
    user: name=admin groups=sudo shell=/bin/bash password=$7$ZIJUvGwr$empMJ4r1JUGcxmjxtTBfTpIdO95JBTJO2/BtD23F2Rfeg2rqN.8t1v3ePPXVl.W7yal2fvrtbJ0T18YwCXmbh0
 
  - name: Add SSH keys to remote hosts
    authorized_key: user=admin key="{{ lookup('file', "~/Downloads/key.pub") }}"
 

Теперь можно запускать выполнение набора инструкций командой:

# ansible-playbook playbooks/useradd.yml --vault-password-file=vault.txt



==========================================
 файлы с переменными групп хранятся в директории                group_vars/имя_группы
 файлы с переменными хостов в директории                        hosts_vars/имя_хоста
 файлы с переменными роли (о них речь пойдет ниже) в директории имя_роли/vars/имя_задачи.yml

Роли

 Ролью называется типовой набор переменных и задач, назначаемых для одного или нескольких серверов. 
 Если вам нужно применить к серверу или группе серверов типовой набор операций, вам достаточно просто назначить ему роль. 
 Предварительно в проекте каталоге проекта должна быть создана соответствующая структура. В сценариях роли назначаются следующим образом:

 -----------------------------
 --- 
- name: check and apply basic configuration to all hosts
  hosts: all
  roles:
    - common

- name: check and apply configuration to group1
  hosts: group1
  roles:
    - pgsql

- name: check and apply configuration to group2
  hosts: group2
  roles:
    - fooapp
----------------------------------

Структура проекта

├── production                # инвентарный файл для продакшн-серверов
├── stage                     # инвентарный файл для stage-окружения
│
├── group_vars/
│   ├── group1                # здесь назначаются переменные для
│   └── group2                # конкретных групп
├── host_vars/
│   ├── hostname1             # специфические переменные для хостов в
│   └── hostname2             # случае необходимости прописываются здесь
│
├── site.yml                  # основной сценарий
├── webservers.yml            # сценарий для веб-сервера
├── dbservers.yml             # сценарий для сервера базы данных
│
└── roles/
    ├── common/               # здесь описываются роли
    │   ├── tasks/            #
    │   │   └── main.yml      # - файл задач роли, может включать файлы
    │   │                     #   меньшего размера
    │   ├── handlers/         #
    │   │   └── main.yml      # - файл с обработчиками (handlers)
    │   ├── templates/        # - директория для шаблонов, в данном
    │   │   └── ntp.conf.j2   #   случае - для конфига ntp
    │   ├── files/            #
    │   │   ├── bar.txt       # - файл-ресурс для копирования на хост
    │   │   └── foo.sh        # - скрипт для выполнения на удалённом хосте
    │   └── vars/             #
    │       └── main.yml      # - ассоциированные с ролью переменные
    │
    ├── pgsql/                # такая же структура, как выше, для роли pgsql
    └── fooapp/               # такая же структура, как выше, для роли fooapp

----------------------------------------------
PLAYBOOK

---
- name: install postgresql 9.3 # имя playbook'a
  # секция, описывающая параметры, которые нужно уточнить у пользователя в начале запуска
  vars_prompt:
    hosts: "Please enter hosts group name" # спрашиваем имя группы серверов в инвентаре (в нашем случае файл $ANSIBLE_HOSTS)
    username: "Please enter username for auth" # спрашиваем имя пользователя для подключения к серверам
  hosts: $hosts # 
  user: $username
  sudo: True
  accelerate: true
  vars:
    app_username: 'app_user'     # имя пользователя мифического приложения, которое работать с базой данных
    app_host_ip: '192.168.0.100' # ip-адрес хоста с запущенным приложением, с него будут поступать запросы в базу данных
    app_database_name: 'appdb'   # имя базы данных приложения

  tasks:
      # Проверяем установлен ли и устанавливаем пакет python-software-properties
      # для обеспечения работы модуля apt. Параметры модуля:
      # pkg - имя пакета для установки
      # state - устанавливаем последнюю версию пакета, 
      # update_cache - обновляем список доступных пакетов перед установкой
    - name: check add-apt-repository 
      apt: pkg=python-software-properties state=latest update_cache=yes

      # добавляем ключ официального apt-репозитория проекта postgresql
      # Параметры модуля:
      # url - URL до файла с ключём
      # state - добавить ключ
    - name: add apt key
      apt_key: url=http://apt.postgresql.org/pub/repos/apt/ACCC4CF8.asc state=present

      # добавляем репозиторий, адрес формируется на основе имени релиза установленной ОС
    - name: add apt repo
      apt_repository: repo='deb http://apt.postgresql.org/pub/repos/apt/ ${ansible_lsb.codename}-pgdg main'

      # устанавливаем пакет с ключём для последующего возможного автоматического обновления
    - name: install pgdg-key
      apt: pkg=pgdg-keyring state=latest update_cache=yes

      # устанавливаем пакеты postgresql-9.3 (непосредственно сам сервер баз данных)
      # и python-psycopg2 - для работы модулей postgresql_user, postgresql_db, postgresql_privs
    - name: install packages
      apt: pkg=$item state=latest
      with_items:
        - postgresql-9.3
        - python-psycopg2
        - python-keyczar

      # создаём пользователя для работы нашего мифического приложения c атрибутом LOGIN
      # сгенерированный пароль будет сохранён в credentials/имя_хоста/postgres/имя_пользователя
    - name: create postresql user for some app
      # выполнение задачи будем производить с правами пользователя postgres (создаётся при установке postgresql)
      sudo: yes
      sudo_user: postgres 
      postgresql_user:
          user=${app_username}
          password="{{ lookup('password','example/credentials/' + inventory_hostname + '/postgres/' + app_username, length=15) }}"
          role_attr_flags=LOGIN

      # создаём базу данных для мифического приложения с говорящими за себя параметрами
    - name: create db for our app
      sudo: yes
      sudo_user: postgres
      action: postgresql_db name=${app_database_name} owner=${app_username} encoding='UTF8' lc_collate='en_US.UTF-8' lc_ctype='en_US.UTF-8' template='template0' state=present

      # Следующая задача будет выполнена хосте приложения, а не на текущем настраиваемом хосте
    - name: add app_user password to .pg_pass file on server with our app
      sudo: yes
      sudo_user: ${app_username}
      delegate_to: ${app_host_ip}
      lineinfile:
          dest=/home/${app_username}/.pgpass
          regexp='^{{ inventory_hostname }}\:\*\:${app_database_name}\:${app_username}'
          line='{{ inventory_hostname }}:*:${app_database_name}:${app_username}:{{ lookup('password','example/credentials/' + inventory_hostname + '/postgres/' + app_username, length=15) }}'
          create=yes
          state=present
          backup=yes

      # добавляем в pg_hba.conf строчку, описываюшую разрешение подключение с ip-адреса приложения для ранее созданной базы и пользователя
    - name: add entry to pg_hba.conf
      lineinfile:
          dest=/etc/postgresql/9.3/main/pg_hba.conf
          regexp='host ${app_database_name} ${app_username} ${app_host_ip}/32 md5'
          line='host ${app_database_name} ${app_username} ${app_host_ip}/32 md5' state=present
      # если файл изменился, то вызовем задачу по перечитыванию конфига postgresql
      # напоминаем что модули ansible возвращают состояние "изменилось/не изменилось" после выполнения,
      # хэндлеры описываются либо в конце playbook'a или в отдельном файле
      notify:
        - reload postgres

      # по умолчанию postgresql слушает только localhost
      # изменияем соответствующий параметр в postgresql.conf на ip-адрес сервера
    - name: add entry to postgresql
      lineinfile:
          dest=/etc/postgresql/9.3/main/postgresql.conf
          regexp='^listen_addresses'
          line="listen_addresses = '${ansible_default_ipv4.address}'"
          state=present
      # если файл изменился, то вызовем задачу по перезапуску postgresql, т.к.
      # параметр listen_addresses можно изменить только перезагрузкой сервера postgresql
      notify:
        - restart postgres

  # описание хэндлеров
  handlers:
      # перечитываем конфигурацию postgresql
    - name: reload postgres
      sudo: yes
      action: service name=postgresql state=reloaded

      # перезагружаем postgresql
    - name: restart postgres
      sudo: yes
      action: service name=postgresql state=restarted


==========================================