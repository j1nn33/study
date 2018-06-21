https://github.com/geerlingguy/ansible-for-devops


---
2 - hosts: all
3 tasks:
4 - name: Ensure NTP (for time synchronization) is installed.
5 yum: name=ntp state=installed
6 - name: Ensure NTP is running.
7 service: name=ntpd state=started enabled=yes
#####################

WWW APP1 ___
            |___ DB 
WWW APP2 ___|
            
=================================
# copy ssh key into servers

#Генерация SSH-ключа на сервере ansible

ssh-keygen -C "$(whoami)@$(hostname)-$(date -I)"

#Если при генерации ключа на все вопросы был дан стандартный ответ (клавишей Enter), 
#то в каталоге ~/.ssh/ появится два файла — id_rsa (закрытый ключ) и id_rsa.pub (открытый ключ).

#Открытый ключ нужно скопировать на удаленный сервер, 
#это можно сделать с помощью команды ssh-copy-id, например так:
ssh-copy-id root@192.168.10.5    

#user - пользователь на удаленном сервере
=================================

			Inventory file 
---------------------------------
# Application servers
[app]
192.168.10.4
192.168.10.5

# Database server
[db]
192.168.10.6

# Group 'multi' with all servers
[multi:children]
app
db

# Variables that will be applied to all servers
[multi:vars]
ansible_ssh_user=root

---------------------------------
=================================
			ad-hoc commands:
• Apply patches and updates via yum, apt, and other package managers.
• Check resource usage (disk space, memory, CPU, swap space, network).
• Check log files.
• Manage system users and groups.
• Manage DNS settings, hosts files, etc.
• Copy files to and from servers.
• Deploy applications or run application maintenance.
• Reboot servers.
• Manage cron jobs.
---------------------------------
# CONFIGURE ALL
ansible multi -a "hostname"
ansible multi -a "df -h"
ansible multi -a "free -m"
ansible multi -a "date"

ansible multi -m yum -a "name=ntp state=installed"
ansible multi -m service -a "name=ntpd state=started enabled=yes"
ansible multi -a "service ntpd stop"
ansible multi -a "ntpdate -q 0.rhel.pool.ntp.org"
ansible multi -a "service ntpd start"
ansible multi -m yum -a "name=epel-release"

# CONFIGURE APP
ansible app -m yum -a "name=MySQL-python state=present"
ansible app -m yum -a "name=python-setuptools state=present"
#ansible app -m yum -a "name=python34"
#ansible app -m yum -a "name=python34-pip"
ansible app -m yum -a "name=python-pip"
#ansible app -m easy_install -a "name=django"
#ansible app -m pip3 -a "name=django"
ansible app -m pip -a "name=django version=1.8 state=present"
ansible app -a "python -c 'import django; print django.get_version()'"

# CONFIGURE DB
ansible db -m yum -a "name=mariadb-server state=present"
ansible db -m service -a "name=mariadb state=started enabled=yes"
ansible db -a "iptables -F"
ansible db -a "iptables -A INPUT -s 192.168.10.0/24 -p tcp -m tcp --dport 3306 -j ACCEPT"
ansible db -m yum -a "name=MySQL-python state=present"
ansible db -m mysql_user -a "name=django host=% password=12345 priv=*.*:ALL state=present"

# Manage users and groups

ansible app -m group -a "name=admin state=present"
ansible app -m user -a "name=johndoe group=admin createhome=yes"
# remove account 
ansible app -m user -a "name=johndoe state=absent remove=yes"

# Manage files and directories
# Get information about a file
ansible multi -m stat -a "path=/etc/environment"
# Copy a file to the servers
ansible multi -m copy -a "src=/etc/hosts dest=/tmp/hosts"
# Retrieve a file from the servers
ansible multi -m fetch -a "src=/etc/hosts dest=/tmp"
# Create directories and files
ansible multi -m file -a "dest=/tmp/test mode=644 state=directory"
# Create symlink
ansible multi -m file -a "src=/src/symlink dest=/dest/symlink owner=root group=root state=link"
# Delete directories and files
ansible multi -m file -a "dest=/tmp/test state=absent"

# Check log files
ansible multi -a "tail /var/log/messages"

# Manage cron jobs
# run a shell script on all the servers every day at 4 a.m., add the cron job with
ansible multi -m cron -a "name='daily-cron-all-servers' hour=4 job='/path/to/daily-script.sh'"
# remove crone job
ansible multi -s -m cron -a "name='daily-cron-all-servers' state=absent"

---------------------------------
			Ansible Playbooks
---
- hosts: all
  tasks:
 
  - name: Install Apache.
    command: yum install --quiet -y httpd httpd-devel
 
  - name: Copy configuration files.
    command:  cp /path/to/config/httpd.conf /etc/httpd/conf/httpd.conf
 
  - command: cp /path/to/config/httpd-vhosts.conf /etc/httpd/conf/httpd-vhosts.conf
 
  - name: Start Apache and configure it to run at boot.
    command: service httpd start
  - command: chkconfig httpd on
---------------------------------
# тотже playbook только с переменными

---
- hosts: all
  tasks:
  - name: Install Apache.
    yum: name={{ item }} state=present
    with_items:
    - httpd
    - httpd-devel
    - name: Copy configuration files.
      copy:
        src: "{{ item.src }}"
        dest: "{{ item.dest }}"
        owner: root
        group: root
        mode: 0644
      with_items:
      - {
        src: "/path/to/config/httpd.conf",
        dest: "/etc/httpd/conf/httpd.conf"
        }
      - {
        src: "/path/to/config/httpd-vhosts.conf",
        dest: "/etc/httpd/conf/httpd-vhosts.conf"
        }
      - name: Make sure Apache is started and configure it to run at boot.
        service: name=httpd state=started enabled=yes


=================================
playbook: CentOS Node.js app server
=================================
install_node_js.yml

---
- hosts: app
  tasks:
  - name: Import EPEL and Remi GPG keys.
    rpm_key: "key={{ item }} state=present"
    with_items:
    - "https://fedoraproject.org/static/0608B895.txt"
    - "http://rpms.famillecollet.com/RPM-GPG-KEY-remi"

  - name: Install EPEL and Remi repos.
    command: "rpm -Uvh --force {{ item.href }} creates={{ item.creates }}"
    with_items:
    - {
    href: "http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.no16 arch.rpm",
    creates: "/etc/yum.repos.d/epel.repo"
      }
    - {
     href: "http://rpms.famillecollet.com/enterprise/remi-release-6.rpm",
     creates: "/etc/yum.repos.d/remi.repo"
      }
 
  - name: Disable firewall (since this is a dev environment).
    service: name=iptables state=stopped enabled=no
  
  - name: Install Node.js and npm.
    yum: name=npm state=present enablerepo=epel

  - name: Install Forever (to run our Node.js app).
    npm: name=forever global=yes state=latest

=================================
# тестирование приложения app.js
// Load the express module.
var express = require('express'),
app = express.createServer();

// Respond to requests for / with 'Hello World'.
app.get('/', function(req, res){
res.send('Hello World!');
});

// Listen on port 80 (like a true web server).
app.listen(80);
console.log('Express server started successfully.');

===========================================
# Basic LAMP server setup with DRUPAL
# https://github.com/geerlingguy/ansible-for-devops, in the drupal directory.

------------------------------------------
vars.yml

---
# The core version you want to use (e.g. 8.5.x, 8.6.x).
drupal_core_version: "8.5.x"

# The path where Drupal will be downloaded and installed.
drupal_core_path: "/var/www/drupal-{{ drupal_core_version }}-dev"

# The resulting domain will be [domain].test (with .test appended).
domain: "drupal"

# Your Drupal site name.
drupal_site_name: "Drupal Test"
------------------------------------------
---
- hosts: all

  vars_files:
    - vars.yml

  pre_tasks:
    - name: Update apt cache if needed.
      apt: update_cache=yes cache_valid_time=3600

  handlers:
    - name: restart apache
      service: name=apache2 state=restarted

  tasks:
    - name: Get software for apt repository management.
      apt: "name={{ item }} state=present"
      with_items:
        - python-apt
        - python-pycurl

    - name: Add ondrej repository for later versions of PHP.
      apt_repository: repo='ppa:ondrej/php' update_cache=yes

    - name: "Install Apache, MySQL, PHP, and other dependencies."
      apt: "name={{ item }} state=present"
      with_items:
        - git
        - curl
        - unzip
        - sendmail
        - apache2
        - php7.1-common
        - php7.1-cli
        - php7.1-dev
        - php7.1-gd
        - php7.1-curl
        - php7.1-json
        - php7.1-opcache
        - php7.1-xml
        - php7.1-mbstring
        - php7.1-pdo
        - php7.1-mysql
        - php-apcu
        - libpcre3-dev
        - libapache2-mod-php7.1
        - python-mysqldb
        - mysql-server

    - name: Disable the firewall (since this is for local dev only).
      service: name=ufw state=stopped

    - name: "Start Apache, MySQL, and PHP."
      service: "name={{ item }} state=started enabled=yes"
      with_items:
        - apache2
        - mysql

    - name: Enable Apache rewrite module (required for Drupal).
      apache2_module: name=rewrite state=present
      notify: restart apache

    - name: Add Apache virtualhost for Drupal 8.
      template:
        src: "templates/drupal.test.conf.j2"
        dest: "/etc/apache2/sites-available/{{ domain }}.test.conf"
        owner: root
        group: root
        mode: 0644
      notify: restart apache

    - name: Symlink Drupal virtualhost to sites-enabled.
      file:
        src: "/etc/apache2/sites-available/{{ domain }}.test.conf"
        dest: "/etc/apache2/sites-enabled/{{ domain }}.test.conf"
        state: link
      notify: restart apache

    - name: Remove default virtualhost file.
      file:
        path: "/etc/apache2/sites-enabled/000-default.conf"
        state: absent
      notify: restart apache

    - name: Adjust OpCache memory setting.
      lineinfile:
        dest: "/etc/php/7.1/apache2/conf.d/10-opcache.ini"
        regexp: "^opcache.memory_consumption"
        line: "opcache.memory_consumption = 96"
        state: present
      notify: restart apache

    - name: Remove the MySQL test database.
      mysql_db: db=test state=absent

    - name: Create a MySQL database for Drupal.
      mysql_db: "db={{ domain }} state=present"

    - name: Create a MySQL user for Drupal.
      mysql_user:
        name: "{{ domain }}"
        password: "1234"
        priv: "{{ domain }}.*:ALL"
        host: localhost
        state: present

    - name: Download Composer installer.
      get_url:
        url: https://getcomposer.org/installer
        dest: /tmp/composer-installer.php
        mode: 0755

    - name: Run Composer installer.
      command: >
        php composer-installer.php
        chdir=/tmp
        creates=/usr/local/bin/composer
    - name: Move Composer into globally-accessible location.
      shell: >
        mv /tmp/composer.phar /usr/local/bin/composer
        creates=/usr/local/bin/composer
    - name: Check out drush 8.x branch.
      git:
        repo: https://github.com/drush-ops/drush.git
        version: 8.x
        dest: /opt/drush

    - name: Install Drush dependencies with Composer.
      shell: >
        /usr/local/bin/composer install
        chdir=/opt/drush
        creates=/opt/drush/vendor/autoload.php
    - name: Create drush bin symlink.
      file:
        src: /opt/drush/drush
        dest: /usr/local/bin/drush
        state: link

    - name: Check out Drupal Core to the Apache docroot.
      git:
        repo: http://git.drupal.org/project/drupal.git
        version: "{{ drupal_core_version }}"
        dest: "{{ drupal_core_path }}"

    - name: Install Drupal dependencies with Composer.
      shell: >
        /usr/local/bin/composer install
        chdir={{ drupal_core_path }}
        creates={{ drupal_core_path }}/vendor/autoload.php
    - name: Install Drupal.
      command: >
        drush si -y --site-name="{{ drupal_site_name }}"
        --account-name=admin
        --account-pass=admin
        --db-url=mysql://{{ domain }}:1234@localhost/{{ domain }}
        --root={{ drupal_core_path }}
        creates={{ drupal_core_path }}/sites/default/settings.php
      notify: restart apache

    # SEE: https://drupal.org/node/2121849#comment-8413637
    - name: Set permissions properly on settings.php.
      file:
        path: "{{ drupal_core_path }}/sites/default/settings.php"
        mode: 0744

    - name: Set permissions properly on files directory.
      file:
        path: "{{ drupal_core_path }}/sites/default/files"
        mode: 0777
        state: directory
        recurse: yes
------------------------------------------
/templates/drupal.test.conf.j2

<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    ServerName {{ domain }}.test
    ServerAlias www.{{ domain }}.test
    DocumentRoot {{ drupal_core_path }}
    <Directory "{{ drupal_core_path }}">
        Options FollowSymLinks Indexes
        AllowOverride All
    </Directory>
</VirtualHost>
==========================================

