#### Теория 
#### Сбор логов с локольного volume
#### Отправка логов по REST
####

###### Теория 
```
Приложение свои логи должно выдавать на stdout и stderr
Дальше система эти данные помещает в файлы на той ноде, где запущен контейнер с приложением. 
Если контейнер мигрирует на другую ноду, его логи будут помещаться в файловую систему этой ноды кластера. 
Как собирать такие логи было показано ./K8S/infra/ELK/README.md (Сбор логов с кластера)

Когда нет возможности запустить контейнер сборщика логов с доступом к локальной файловой системе кластера kubernetes.
И в этом случае у вас не будет доступа к файлам с логами.

Решить проблему можно следующим образом:
    1 Сбор логов с локольного volume
    2 Отправка логов по REST

```
###### Сбор логов с локольного volume
```
- ./K8S/infra/ELK/image/app_log.png
- Добавляем в контейнере локальный volume для логов.
- Подключаем этот volume к приложению.
- Настраиваем приложение, что бы оно выдавало логи и на stdout и писало их в файл в локальный volume.
- Добавляем в под контейнер с приложением сбора логов.
- Подключаем к новому контейнеру локальный volume с логами.

Пример на основе https://github.com/BigKAA/youtube/blob/master/hazelcast/README.md

- АРР помещает логи на стандарный вывод и пишет их в локальный volume
- fluenbit читает логи из локального volume и отправляет их наржу 
- APP и fluenbit (sidecar) - в одном pod
```
```bash
# необходимо изменить конфигурацию log4j. самого приложения 
# ---
appenders = console, file
rootLogger.level=${env:LOGGING_LEVEL}
rootLogger.appenderRefs= STDOUT, RollingFile 
rootLogger.appenderRef.stdout.ref=STDOUT
rootLogger.appenderRef.file.ref=RollingFile
appender.file.type=RollingFile
appender.file.name=RollingFile
appender.file.fileName=${env:LOG_FILE_PATH}/${env:LOG_FILE}.log                            # имя файла 
appender.file.filePattern=${env:LOG_FILE_PATH}/${env:LOG_FILE}-%d{yyyy-MM-dd}-%i.log.gz    # шаблон для ротации логов
appender.file.layout.type=JsonLayout
appender.file.layout.compact=true
appender.file.layout.eventEol=true
appender.file.policies.type=Policies
appender.file.policies.time.type=TimeBasedTriggeringPolicy
appender.file.policies.time.interval=1
appender.file.policies.time.modulate=true
appender.file.policies.size.type=SizeBasedTriggeringPolicy
appender.file.policies.size.size=50MB
appender.file.strategy.type=DefaultRolloverStrategy
appender.file.strategy.max=3
# ---
# В конфиге использованы две переменные среды окружения, которых нет в изначальном чарте: LOG_FILE_PATH и LOG_FILE.
# ---
# Additional Environment variables
  env:
    - name: LOG_FILE
      value: hazelcast
    - name: LOG_FILE_PATH
      value: /data/external
# ---

# Включим поддержку локального volume:
# ---
# externalVolume is the configuration for any volume mounted as '/data/external/'
  externalVolume:
    emptyDir: {}
#---

# Конфигурация fluentbit
#---
        [INPUT]
            Name              tail
            Tag               ${infsystem}-${env}-${suffix}-${APP_NAME}.*
            Parser            podapp
            Path              ${LOG_FILE_PATH}/${LOG_FILE}.log                     # Какие логи читать 
            DB                ${LOG_FILE_PATH}/${LOG_FILE}.log.db                  # В какую базу данных сохранять 
            Mem_Buf_Limit     50MB
            Refresh_Interval  10
            Skip_Long_Lines   On

        [FILTER]                                                                   # Настройка модификатора логов 
            Name              modify
            Match             ${infsystem}-${env}-${suffix}-${APP_NAME}.*          # 
            set app           ${APP_NAME}                                          # установка имени приложения 
            set mamespace     ${APP_NAMESPACE}                                     # установка namespace приложения 
            set host          ${APP_NODENAME}                                      # установка nodename приложения 
            set pod           ${APP_POD}                                           # установка pod приложения 

        [OUTPUT]                                                                   # куда логи отправлять                     
            Name              stdout
            Match             *
            Host              ${FLUENT_ELASTICSEARCH_HOST}
            Port              ${FLUENT_ELASTICSEARCH_PORT}
#---
```
###### Отправка логов по REST
######