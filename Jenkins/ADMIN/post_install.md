##### greenball
##### Jenkins Plugin Installation
#####


###### greenball
```
```
######
```
Jenkins Plugin Installation
● Web UI
● CLI
● /var/lib/Jenkins/plugins

Jenkins Plugin. Most Useful
● Rebuilder
● Config File Provider
● Ansi Color
● Active Choice


Установка plugin 

java -jar /usr/local/bin/jenkins-cli.jar -auth admin:1192f0371dbd65b5ba24d1525ecabe47f1 -s http://192.168.1.70:8080/ -webSocket install-plugin AnsiColor


/var/lib/Jenkins/plugins

отключить плагин можно как из GUI так и на файловой система
drwxr-xr-x  7 jenkins jenkins     4096 Mar 12 11:31 email-ext/
-rw-r--r--  1 jenkins jenkins   961517 Mar 12 11:31 email-ext.jpi
-rw-r--r--  1 jenkins jenkins        0 Mar 12 18:42 email-ext.jpi.disabled

```
######
```
```
######
```
```