Время в контейнерах идет по хостовой машине 
По умолчанию timezone UTC

Два решения:
```
1 - способ (не править контейнер, поправку делать в fluenbit-conf)
./K8S/infra/ELK/source/fluentbit-cm.yaml
---
  parsers.conf: |
    [PARSER]
        Time_Offset +0300
---
```

2 - способ Изменить timezone в контейнере. 
Для этого, в самом контейнере должен быть установлен пакет tzdata. Если его нет, то см. способ 1

```
Добавить в контейнер необходимый пакет. Лучше всего это сделать на стадии создания образа

---
FROM alpine:latest
RUN apk update && \
    apk add --no-cache tzdata
---
После того как контейнер добавлен, для смены timezone ему достаточно передать переменную среды окружения TZ

./K8S/useful/timezone/app_tz.yaml
env:
    - name: "TZ"
    value: "Europe/Moscow"

```
