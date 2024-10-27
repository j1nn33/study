
#### change password
#### cli
#### job import/export


###### change password
```
cat /var/lib/jenkins/credentials.xml

# идем
http://<IP>:8080/manage/script
println(hudson.util.Secret.decrypt("{AQAAABAAAA......}"))

```
###### cli
```
# Консольные команды Jenkins
# /Настроить Jenkins/Jenkins CLI 

sudo wget http://127.0.0.1:8080/jnlpJars/jenkins-cli.jar -P /usr/local/bin/

java -jar /usr/local/bin/jenkins-cli.jar -auth <имя пользователя>:<пароль> -s http://127.0.0.1:8080/ <выполняемые команды и опции>

java -jar /usr/local/bin/jenkins-cli.jar -auth admin:<пароль> -s http://<IP>:8080/ -webSocket help

# Конфигурируем токен
# (свойства пользователя) user/configure

java -jar /usr/local/bin/jenkins-cli.jar -auth admin:1192f0371... -s http://<IP>:8080/ -webSocket help
java -jar /usr/local/bin/jenkins-cli.jar -auth admin:1192f0371... -s http://<IP>:8080/ -webSocket version

# Установка plugin 

java -jar /usr/local/bin/jenkins-cli.jar -auth admin:1192f0371dbd65b5ba24d1525ecabe47f1 -s http://<IP>:8080/ -webSocket install-plugin AnsiColor
```
#### job import/export
```
http://<IP>:8080/jnlpJars/jenkins-cli.jar

java -jar jenkins-cli.jar -s http://JENKINS_USER:JENKINS_PASSWORD@JENKINS_IP:JENKINS_PORT get-job sampleJob > sampleJob.xml
java -jar jenkins-cli.jar -s http://JENKINS_USER:JENKINS_PASSWORD@JENKINS_IP:JENKINS_PORT create-job sampleJob < sampleJob.xml6

```
