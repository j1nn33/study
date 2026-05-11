#### ANSIBLE MEMO

nginx_install.yml 
```yaml
- name: Soft install
  hosts: webservers
  become: true
  tasks:
    - name: Install
      ansible.builtin.apt:
        name: nginx
        state: present

    - name: Change nginx.conf
      ansible.builtin.copy:
        src: files/nginx.conf
        dest: /etc/nginx/nginx.conf
        mode: '0644'
        owner: nginx
        group: nginx
		
```
ansible-playbook nginx_install.yml

#### YAML
```
--- В начале файла указываются
#   Комментарии 
    Отсутпы состоят из двух пробелов
Булевы выражения - маленкими буквами
```
Списки (или последовательности) оформляются с помощью отступов и дефиса:

```
need_support_soft:
  - xrdp
  - tree
  - mc
  - wget
``` 
  

Словари (или отображения) 
```
address:
  street: Lenina
  city: Moscow
```  

```
address: { street: Lenina, city: Moscow}
```

Многострочные значения поддерживаются через распознавание оператторных скобок (| и >), 
символы начала многострочного текста (+ и -) и отступы (от 1 до 9) 
 
```
---
visiting_address: |+
  Department of Computer Science
  
  A.V. Williams Building
  University of Maryland


```

#### ПЕРЕМЕННЫЕ 

задаваться прямо в сценарии
```
vars:
  key_file: nginx.key
  conf_file: /etc/nginx/sites-available/default
  
- name: Nginx config install
    ansible.builtin.copy:
      src: files/nxinx.conf
      dest: "{{ conf_file }}"

```
в отдельных файлах

```
vars_files:
  nginx.yml
```
разместить все переменные относящиеся к роли в файле defaults/main.yml

посмотреть значение переменной 
```
- debug: var=varname

debug:
  msg: "The URL is {{ server_name ~'.'~ domain.name }}"
  
```
опрелелить переменную во время работы
```
- name: Whoami found
  command: whoami
  register: login
  
- debug: var=login
- debug: msg="You are {{ login.stdout }}"  
```
Ansible из командной строки с параметрами -e var=value. Также можно передать целый файл с переменными -e @filename.yml

#### Шаблоны

```
deb https://download.software/ubuntu/{{ ubuntu_version }} {{ ubuntu_codename }} main

```
#### Циклы

```
- name: Copy TLS
  ansible.builtin.copy:
    src: "{{ item }}"
    dest: "{{ tls_dir }}"
  loop:
    - "{{ key_file }}"
    - "{{ cert_file }}"
  notify: Restart nginx

```
#### Обработчики

```
handlers:
  - name: Restart nginx
    service:
      name: nginx
      state: restarted

```
##### inventory
```
inventory/hosts.yml

all:
  children:  
    prod:
      children:
        webservers:
          hosts:
            test01:
              ansible_host: 10.10.10.4
            test02:
              ansible_host: 10.10.10.5
```
группы all, prod и webservers. 
При этом prod и webservers являются дочерними от all, а webservers является дочерней от prod.
То есть если указать для сценария вышестоящий уровень, то он будет применён и к нижестоящим, но не наоборот.


Выбор хостов для применения

```
all или * - все хосты
dev:stage - объединение групп
dev:&stage - выбор только общих хостов для двух групп
dev:!stage - только уникальные хосты из первой группы
*.test.com - шаблон
test[1:5].com - шаблон с диапазоном
~web\d\/test\.(com|ru) - регулярное выражение

```

#### Роли
ansible-galaxy init --init-path playbooks/roles ansible_install


```
defaults/main.yml - переменные по умолчанию
files/main.yml - файлы для загрузки на хосты
handlers/main.yml - обработчики
meta/main.yml - информация о роли
tasks/main.yml - точка входа
templates/angie.conf.j2 - шаблоны для загрузки на хосты
vars/main.yml - переменные, которые переопределять нежелательно

```
задачи которые необходимо выполнить до и после роли
```
pre_tasks:
  - name: Update apt cache
    apt:
      update_cache: true
      
roles:
  - role...
    
post_tasks:
  - name: Notify to Telegram
    ...

```

#### Фильтры

```
# default
host: "{{ database_host | default('localhost') }}"

# pash & file_name

vars:
  homepage: /usr/nginx/html/index.html
  
- name: Copy home page
  copy:
    src: "files/{{ homepage | basename }}"
    dest: "{{ homepage }}"

```
#### Подключение задач и ролей

```
nginx_install.yml


- name: Nginx install
  package:
    name: nginx
    
- name: Nginx start
  service:
    name: nginx
    state: started
    enabled: true

# при необходимости добавить его

- include_tasks: nginx_install.yml

- name: Platform specific actions
  include_tasks: "{{ ansible_os_family }}.yml"
  
# Подключение ролей

- name: Install web
  include_role
    name: nginx

# указать с какого таска начинать выполнение

- name: Install php
  include_role
    name: php
    tasks_from: install
	
	
```

#### Блоки
При выполнении задач есть возможность группировать их по блокам, это позволяет 
определять условия выполнения и аргументы для всех задач сразу
```
- block:
  - name: Nginx install
    ...
    
  - name: Nginx start
    ...
when: ansible_os_family == 'RedHat'

# обработка ошибок
- block:
    ...
    - debug: msg="You never see this message"
  rescue:
    - debug: msg="You see this message in case of failure in the block"
  always:
    - debug: msg="This will be always executed"

```

#### Выполнение задач на машине отличной от целевой

скачать файл, но на удалённом хосте нет доступа в интернет. 
можем скачать его на свой управляющий ПК и потом передать куда нужно.
```
- name: Download test binary
  delegate_to: localhost
  connection: local
  become: false
  get_url:
    url: "https://test.com"
    dest: "~/Downloads/test"
    mode: '0755'
  ignore_errors: true
```
#### Лимитировать выполнение на хостах

```
# обрабатываться один хост за раз.

- name: Upgrade package
  hosts: web
  serial: 1
  
# max_fail_percentage. В нём будет учитываться количество неудачных выполнений задачи и в связке с serial можно остановить выпонение при заданном пороге ошибок.

# указать проценты 

# выполнить установку на одном хосте, потом на половине, а потом и на всех
serial:
  - 1
  - 50%
  - 100%

  
# Если задачу нужно выполнить разово, то поможет выражение run_once: true.
# Флаг --step при запуске ansible-playbook заставляет Ansible запрашивать подверждение на запуск каждой задачи.

```
#### Теги

```
- name: Download test binary
  get_url:
    url: "https://test.com"
    dest: "~/Downloads/test"
    mode: '0755'
  tags:
    - first
```
Запускать только таски с нужным тегом --tags first 
пропускать их --skip-tags.

#### Стратегии выполнения

```
#  Ansible использует стратегию линейного выполнения (linear), это значит, 
что задача запускается на всех хостах сразу, ждёт результата и двигается дальше. 
Но данное поведение можно изменить. Если указать стратегию free, то Ansible не будет ждать окончания опреаций на других хостах.

- name: Strategies
  hosts: web
  strategy: free
```








