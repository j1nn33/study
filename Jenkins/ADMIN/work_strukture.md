### work_strukture
### Пример
##### work_strukture
```
Описание структуры для запуска джобы которая запускает ansible-role
```
#####
```
Repository URL  - ссылка на репу 
Script_path     - ./study/Jenkins/Project/Jenkins/temp.groovy

--
--Project
  |_Jenkins/temp.groovy
  |
  |__<name_job>
       |__Jenkins/temp.groovy                # groovy for jenkins_job
       |__Ansible
          |__inventories
               |__dev/all.yaml
               |__ift/all.yaml
          |__plabook
               |__roles
                  |__role_name
                     |__tasks/main.yaml 
               |__<role_name>.yaml
```
#####
```
./Jenkins/Project
```