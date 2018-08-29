------------------------------------------
# определяем переменные на основе которых будет генерироваться шаблон
# index.html при копировании в предыдущем примере был везде одинаковый
# теперь он будет генерироваться
# переименовываем в index.html (из предыдущего примера) в index.j2
------------------------------------------
index.j2

<font color="green"> server is {{ansible_hostname}}
server os family {{ ansible_os_family }}
ip address {{ ansible_default_ipv4.address }}

# GENERATE index.html file
 - name: GENERATE index.html file
   template: src={{ source_folder}}/index.j2 dest={{ destin_folder}}/index.html mode=0555
   notify:
        - Restart Apache RedHat
        - Restart Apache Debian
------------------------------------------
ROLES
-------------
1 mkdir roles 
2 cd roles/
# выполняем команду для создания дерева каталогов deploy_apache_web
$ ansible-galaxy init deploy_apache_web

/defaults/main.yml 
# Здесь очень удобно задавать какие-то общие вещи, например по умолчанию хост для БД localhost, а 
# group_vars/host_vars вы можете задавать нужные хосты для соответствующих окружений.

/handlers/main.yml
# В обработчиках можно указывать абсолютно любые действия которые необходимо выполнять 
# после тех или иных тасков, будь то выкладка нового кода или изменение конфига.

/tasks/main.yml
# Файл с описанием тасков
# Можно задавать жесткие условия для выполнения некоторых тасков

------------------------------------------
3 имеем исходный плейбук 
---
- name: Install Apache and Upload simple Web MyWebSite
  hosts: all 
  become: yes
  

  vars:
    source_folder: ./MyWebSite
    destin_folder: /var/www/html

  tasks:
  - block:  # =====BLOCK FOR REDHAT==== 
      - name: Install Apache for RedHat
        yum: name=httpd state=latest
      
      - name: Start Web Server for RedHat
        service: name=httpd state=started enabled=yes

    when: ansible_os_family == "RedHat"
          
  - block:  # =====BLOCK FOR DEBIAN====        
      - name: Install Apache for Debian
        apt: name=apache2 state=latest
    
      - name: Start Web Server for Debian
        service: name=apache2 state=started enabled=yes
    
    when: ansible_os_family == "Debian"

 # GENERATE index.html file
 - name: GENERATE index.html file
   template: src={{ source_folder}}/index.j2 dest={{ destin_folder}}/index.html mode=0555
   notify:
        - Restart Apache RedHat
        - Restart Apache Debian
   
 - name: Copy HomePage for Web Server
   copy: src={{ source_folder}}/{{ item }} dest={{ destin_folder}} mode=0555
   loop:
    - "file1"
    - "file2"
      # ver 2 скопировать всю директорию
      #copy: src={{ item }} dest={{ destin_folder}} mode=0555
      #with_fileglob: "{{ source_folder }}/*.*"
      
   notify:
    - Restart Apache RedHat
    - Restart Apache Debian
  
  handlers:
  - name: Restart Apache RedHat
    service: name=httpd state = restarted
    when: ansible_os_family == "RedHat"

  - name: Restart Apache Debian
    service: name=apache2 state = restarted
    when: ansible_os_family == "Debian"

------------------------------------------ 
4 распихиваем этот плейбук по этой структуре каталогов
------------------------------------------
 1. в vars или defaults
    destin_folder: /var/www/html

 
 2. в files 
  укладываем копируемые на сервер файлы

 3. в handlers

 - name: Restart Apache RedHat
    service: name=httpd state = restarted
    when: ansible_os_family == "RedHat"

 - name: Restart Apache Debian
    service: name=apache2 state = restarted
    when: ansible_os_family == "Debian"

4. в task 
   переносим все из секции task
   (менятеся )
    - name: GENERATE index.html file
   template: src=index.j2 dest={{ destin_folder}}/index.html mode=0555
      
 - name: Copy HomePage for Web Server
   copy: src={{ item }} dest={{ destin_folder}} mode=0555
   

5. templets
   index.j2

6. PLAYBOOK теперь будет таким
---
- name: Install Apache and Upload simple Web MyWebSite
  hosts: all 
  become: yes
  
  roles:
   - deploy_apache_web
   # или если добавить условие для linux
   - { roles: deploy_apache_web, when: ansible_system == 'Linux'}