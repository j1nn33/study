------------------------------------------
----------ЦИКЛЫ  LOOP-------
---
-name: Loops Plabook
 hosts: linux1
 become: yes
 tasks:
 -name: Say Hello to All
 debug: msg="Hello {{ item }}" 
 with_items:
    - "name1"
    - "name2"
    - "name3"
# или 
 loop:
    - "name1"
    - "name2"
    - "name3"

# until loop
# записывает Z (при каждом выполнении команды Z добавляется в конец файла)
# в myfile.txt и выводит его 
# цикл работает до тех пор пока с экрана не будут считаны ZZZZ
  
 -name: Loop Until example
  shell: echo -n Z >> myfile.txt && cat myfile.txt
  register: output
  delay: 2      # задержка по времени
  retries: 10   # всего делать 10 раз
  until: output.stdout.find("ZZZZ") == false

 - name: Print FInal output
   debug:
     var: output.stdout

 - name: Install many pacckages
   yum: name={{ item }} state=installed
   with_items:
        - tree
        - mc
        - wget
-------------------------------
# копируем файлы на сервера на основе БОЛКОВ предыдущего примера
  vars: 
    source_folder: ./MyWebSite
    destin_folder: /var/www/html

  - block:  # =====BLOCK FOR REDHAT==== 
  
      - name: Install Apache for RedHat
        yum: name=httpd state=latest
                     
      - name: Start Web Server for RedHat
        service: name=httpd state=started enable=yes

    when: ansible_os_family == "RedHat"
          
          
  - block:  # =====BLOCK FOR DEBIAN====        

      - name: Install Apache for Debian
        apt: name=apache2 state=latest
    
      - name: Start Web Server for Debian
        service: name=apache2 state=started enable=yes
    
    when: ansible_os_family == "Debian"


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
----------переменые
 
------------------------------------------
ВЫБОР
------------------------------------------
------------ 

------------------------------------------

------------------------------------------

------------------------------------------

------------------------------------------

------------------------------------------