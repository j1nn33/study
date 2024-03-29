---------------------------
Подготовительные мероприятия

1. Собрать состояние до выполнения примения настроек обновления политик
   - запуск bash-script
     - скопировать каталог /bash/report
     - запустить report_script.sh

2. Дополнительный анализ рабочей версии
     - провести ручной анализ файла /etc/krb5.conf и /etc/krb5.conf.d/*
       (при необходимости изменить template krb5.j2)
     - провести анализ /etc/audit/rules.d/ и /etc/rsyslog.d/
        на наличие подобных настроек   
     - провести анализ существующих парольных политик и их приоритет
       (возможно потребуется фикс их параметров)

Примение настроек безопасности

1. Примение политик LDAP
   политики по SSL не применимы (по резульатам теста)
   - запуск bash-script
     - скопировать каталог /bash/update
     - задать переменные в LDAP_security_update.sh
     - запустить LDAP_security_update.sh

2.  Применение политики разрещений на файлы 
    список файлов и разрешениая к ним в ipa_security_update.yml    
    ansible-playbook ipa_security_update.yml -i hosts.ini -k --tags "file-policy"

3.  Применине настроек для /etc/krb5.conf
    ВАЖНО произвести корректировку шаблона если настройка будет применяться на уже работающей IPA
    ansible-playbook ipa_security_update.yml -i hosts.ini -k --tags "krb5-policy"
    
    (под вопросом примениение части политик и перезапуск сервисов ipa)

4.  Применение политик /etc/audit/rules.d/  
    ansible-playbook ipa_security_update.yml -i hosts.ini -k --tags "audit-policy"

5.  Применение политик /etc/rsyslog.d/  
    ansible-playbook ipa_security_update.yml -i hosts.ini -k --tags "rsyslog-policy"    

5.  Применение политик /etc/named.conf  
    ansible-playbook ipa_security_update.yml -i hosts.ini -k --tags "bind-policy"
    allow-update { none; } - устанавливается в zone (в zone "." -не савим)

6.  Применение парольной политики
    При добавление политики: 
      - должна существовать группа
      - приоритет политики должени быть уникальным
    запуск bash-script
     - скопировать каталог /bash/update 
     - запустить pass_policy_update.sh

---------------------------
# Для быстрого тестирования 
# inventory.ini
# ansible.cfg

Запускать 
~./repo/study/ROLES/ipa_security_settings

без ключа
ansible all -i hosts.ini -m ping -k 
с ключем
ansible.cfg   private_key_file = ~/.ssh/id_rsa
ssh-copy-id username@remote_host
ansible all -i hosts.ini -m ping -k
ansible all -i hosts.ini -m shell -a 'ps -ef | grep java'
ansible all -i hosts.ini -m command -a 'systemctl status chronyd.service'

# как запустить
ansible-playbook ./ipa_check_security.yml -i ./hosts.ini -k 


-----------------------------------


План внедрения и тестирования

Результат работ:

Положительный 
 - наличие автоматизации примениения настроек
 - наличие плана работ и отката 
 - наличие продукта соответствующего требованиям 
 - наличие тех.подтверждение соответсвия требованиям  

Промежуточный
 - наличие автоматизации примениения настроек
 - наличие плана работ и отката 
 - наличие продукта соответствующего части требованиям 
 - наличие тех.подтверждение соответсвия части требованиям  
 - наличие обснования о невозможности выполнения части требований
 - наличе рисков и мероприятий по митигации рисков

Негативный
 - наличие автоматизации примениения настроек
 - наличие плана работ и отката 
 - фиксация состояния 
 - наличие обснования о невозможности выполнения требований
 - наличе рисков и мероприятий по митигации рисков

План работ: 

1. развертывание новой инсталяции (согласно требованиям)
2. тестирование новой инсталяции
3. анализ документа и прикидка как его выполянть (1 итерация - разложить настойки по группам и как их тестировать)
4. фиксация ситуации с настройками на новой инсталяции
5. анализ применимости настроек
   
   - мнение эксперной группы СУДИС о применимости тех или иных настроек к нашему случаю
     (в случае не применние - фиксация обоснования причины, регистация риска и сроков устранения)
   - фиксирование потенциальных рисков и влияние на клиентов
   - проработка плана отката
   - проработка плана развертыания на работающей инсталяции с учетом rolling-update
   - получение тех решения, как применять и тестировать настройки
6. разработка и отладка автоматизации примения настроек (возможно сторонний стенд с возможностью отката)
7. валидация автоматзации коллегами и экспертной группой
8. Планирование работ на тестовом стенде (возможно с привлечением коллег из СУДИС)
9. фиксация резултатов и тестироваине результата на тесовом стенде
10. по необходимости возвращение к п. 4
11. Принятие решения о преносе настроек на работающй стенд
12. Проработка плана с учетом плана на работающем стенде 
13. Фиксация результатов и анализ влияния на клиентов
14. наличие плана работ с клиентами 
        
