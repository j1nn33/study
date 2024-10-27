#### ARCHITECTURE
#### установка Jenkins 
#### настройка доступа к управляющему хосту (jenkins-client)
#### Управление slave

###### ARCHITECTURE
```
 Отказоустойчивость 
Loadballancer
      |
   ----------
   |        |
 master   slave 
 
slave - тот же самый мастер к которому по rsync синхронится домашний каталог дженкинса
если master упал то переключаются на slave 

  Backup
для бекапа дженкинса достаточно бекапить домашний каталог     

```
###### установка Jenkins
```

# PREINSTALL CONFIGURE

#Проверяем последние обновления и устанавливаем wget
sudo apt-get update && sudo apt install wget

#Конфигурируем limit. for jenkins user

sudo vi /etc/security/limits.conf
#Добавляем содержимое:

jenkins soft  core unlimited
jenkins hard  hard unlimited
jenkins soft  fsize unlimited
jenkins soft  fsize unlimited
jenkins soft  nofile 4096
jenkins hard  nofile 8192
jenkins soft  nproc 30654
jenkins hard  nproc 30654

# Конфигурируем firewall

sudo apt-get install ufw
sudo ufw allow OpenSSH
sudo ufw allow 8080
sudo ufw enable
# Проверяем java  (рекомендация 11 версия)
java --version

# Если java отсутствует, то устанавливаем
sudo apt install openjdk-11-jre-headless
java --version

# INSTALL JENKINS

https://www.jenkins.io/download/

# Добавляем Jenkins repository
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key |sudo gpg --dearmor -o /usr/share/keyrings/jenkins.gpg
sudo sh -c 'echo deb [signed-by=/usr/share/keyrings/jenkins.gpg] http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'

#Устанавливаем Jenkins
sudo apt-get update
sudo apt-get install jenkins -y
systemctl status jenkins
systemctl enable jenkins
# Конфигурируем дополнительным Java параметры:
sudo vi /lib/systemd/system/jenkins.service

# Добавляем:
# Arguments for the Jenkins JVM

Environment="JAVA_OPTS=-Djava.awt.headless=true -XX:+AlwaysPreTouch -XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/var/lib/jenkins/log -XX:+UseG1GC -XX:+UseStringDeduplication -XX:+ParallelRefProcEnabled -XX:+DisableExplicitGC -XX:+UnlockDiagnosticVMOptions -XX:+UnlockExperimentalVMOptions -Xlog:gc=info,gc+heap=debug,gc+ref*=debug,gc+ergo*=trace,gc+age*=trace:file=/var/lib/jenkins/gc.log:utctime,pid,level,tags:filecount=2,filesize=100M -Xmx512m -Xms512m"


# RUNNING JENKINS

# Запускаем Jenkins
sudo systemctl daemon-reload
sudo systemctl restart jenkins

http://<IP>:8080

В консоле смотрим пароль для инициализации:
cat /var/lib/jenkins/secrets/initialAdminPassword

# сделать зеленые индикаторы greenball (плагины)

```
###### настройка доступа к управляющему хосту (jenkins-client)
```
Требования:
● Наличие JRE/JDK на VM
● SSH/Agent порт открыты и доступны

Best practice:
● Используйте SSH подключение по ключу
● Избегайте использования JNLP через браузер
● Определяйте tools

---------------------
Подключение slave
- через GUI Jenkins
  
  worker - 1 cpu - 1worker (java 2cpu - 1 worker)
  remote root directory : /home/jenkins
  label - метка по которой выбираем агента в pipeline

----------------------------------
# Настройка slave
# - на slave
# Устанавливаем java
apt install openjdk-11-jre-headless
# Создаем пользователя jenkins и задаем для него пароль

sudo useradd -m -s /bin/bash jenkins
sudo passwd jenkins

# - на master
#  смотрим можно ли залогинится пользователем jenkins

cat /etc/passwd
# jenkins:x:111:113:Jenkins,,,:/var/lib/jenkins:/bin/bash  (убрать nologin)
		
#   - переходим на root --> Jenkins 	
su - jenkins
#   - генерируем ключи если их нет .ssh
ls -al
ssh-keygen

#   - все настройки jenkins лежат в директории /var/lib/jenkins
#   - смотрим и копируем ключ cat .ssh/id_rsa.pub
#   - на удаленной машине под root
vi .ssh/authorized_keys  (копируем то что из .ssh/id_rsa.pub)
        
#   - из host jenkins под jenkins
ssh root@<jenkins-client>

cd ~
ssh-keygen -t rsa -f jenkins_slave

cat jenkins_slave
Открываем web-интерфейс Jenkins, переходим в Manage Jenkins-> Manage Credentials (global)
(cm ./kurs/add_slave)

ssh-copy-id -i jenkins_slave.pub jenkins@host

# Открываем web-интерфейс Jenkins, переходим в Jenkins - Manage Jenkins -> Manage Node and Cloud

# для возможности запуска на slave docker
systemctl status docker
usermod -a -G docker jenkins
su - jenkins
docker run hello-world

```
###### Управление slave
```

1 - способ
  - конфигрурить slave под какие либо окруженя и версии (maven,  dotnet)

2 - способ global configuration tool 
  - базовые окружения jеnkins ставит сам

  см  ./kurs/configuration_tool

  включить можно 

pipeline {
    agent { 
        label 'linux'
    }
    tools {
        maven 'maven-3.8.6'     //- maven-3.8.6 должен совпадать с там что указали в configuration_tool
    }
    stages {
        stage("test agent") {
            steps {
                sh 'mvn --version'
            }
        }
    }
}
```
######
```
```
######
```
```
######
```
```
######
```
```
######
```
```
