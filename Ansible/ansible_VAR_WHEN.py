------------------------------------------
----------dialog 
---
- hosts: all

  vars_prompt:
    - name: share_user
      prompt: "What is your network username?"

    - name: share_pass
      prompt: "What is your network password?"
      private: yes

------------------------------------------
----------переменые
 vars:
   message1: hello1
   message2: hello2
   secret: password

 tasks:
 - name: Print secret var
   debug:
     var: secret
 
 - name: Print ver.2
   debug:
     msg: "ВВЕДЕНЫЙ ПАРОЛЬ: {{password}}"

 - set_fact: full_message=" ПРИВЕТ {{message1}} ПРИВЕТ {{message2}}" 
 - debug:
     var: full_message

# сохранение результата в переменную
 
 - shell: uptime
   register: results

 - debug:
     var: results
 
 - debug:
     var: results.stdout

------------------------------------------
ВЫБОР
------------------------------------------
------------ when - SIMPLE
# выводит семейство ОС LINUX
 tasks:
  - name: Check and Print LINUX version
    debug: var=ansible_os_family

  - name: Install Apache for RedHat
    yum: name=httpd state=latest
    when: ansible_os_family == "RedHat"

  - name: Install Apache for Debian
    apt: name=apache2 state=latest
    when: ansible_os_family == "Debian"

  - name: Start Web Server for RedHat
    service: name=httpd state=started enable=yes
    when: ansible_os_family == "RedHat"

  - name: Start Web Server for Debian
    service: name=apache2 state=started enable=yes
    when: ansible_os_family == "Debian"

 ------------------------------------------
------------when - BLOCK
# пример выше реализованный с помощью блоков
vars:
  source_file: ./MyWebSite/index.html
  destin_file: /var/www/html

 tasks:
  - name: Check and Print LINUX version
    debug: var=ansible_os_family
  
  - block:  # =====BLOCK FOR REDHAT==== 
  
      - name: Install Apache for RedHat
        yum: name=httpd state=latest
                     
      - name: Copy HomePage for Web Server
        copy: src={{ source_file}} dest={{ destin_file}} mode=0555
        notify: Restart Apache RedHat
        
      - name: Start Web Server for RedHat
        service: name=httpd state=started enable=yes

     when: ansible_os_family == "RedHat"
          
          
  - block:  # =====BLOCK FOR DEBIAN====        

      - name: Install Apache for Debian
        apt: name=apache2 state=latest
    
      - name: Copy HomePage for Web Server
        copy: src={{ source_file}} dest={{ destin_file}} mode=0555
        notify: Restart Apache Debian

      - name: Start Web Server for Debian
        service: name=apache2 state=started enable=yes
    
    when: ansible_os_family == "Debian"


  handlers:
  - name: Restart Apache RedHat
    service: name=httpd state = restarted
  - name: Restart Apache Debian
    service: name=apache2 state = restarted


------------------------------------------
------------when

- yum: name=mysql-server state=present
    when: is_db_server

- command: my-app --status
    register: myapp_result
- command: do-something-to-my-app
    when: "'ready' in myapp_result.stdout"

# Run 'ping-hosts.sh' script if 'ping_hosts' variable is true.
- command: /usr/local/bin/ping-hosts.sh
    when: ping_hosts

# Downgrade PHP version if the current version contains '7.0'.
- shell: php --version
    register: php_version
- shell: yum -y downgrade php*
    when: "'7.0' in php_version.stdout"
# Copy a file to the remote server if the hosts file doesn't exist.
- stat: path=/etc/hosts
    register: hosts_file
- copy: src=path/to/local/file dest=/path/to/remote/file
    when: hosts_file.stat.exists == false
------------------------------------------
------------wait_for

- name: Wait for webserver to start.
  local_action:
    module: wait_for
    host: "{{ inventory_hostname }}"
    port: "{{ webserver_port }}"
    delay: 10
    timeout: 300
    state: started


-----------------------------------------
