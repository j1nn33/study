
#### Сбор логов с кластера ( отправка логов в ELK )
```
   - описание 
   - установка 
   - проверка 
```
###### описание
```
Сбор логов с кластера на рисунке ./K8S/infra/ELK/image/arch.jpg

ELK   - без ssl
   индексы создаются vector
   - host-%Y-%m-%d     
   - kube-%Y-%m-%d
Kafka 
   - kube   - все логи связанные с k8s
   - host   - все логи системного приложения сервера linux

fluentbit
   - раскидываем сообзения по различным топикам

vector
   - фильтрация техничекских полей сообщений в кафке 

```

###### Установка 
```
- ELK          ./K8S/infra/ELK/OpenSearch/opensearch.md
- Kafka        ./K8S/infra/ELK/Kafka/kafka.md 
- vector       ./K8S/infra/ELK/vector.md   
- fluentbit    ./K8S/infra/ELK/fluentbit.md             (Установка через helm)
```
###### проверка    
```
fluentbit - логи пода смотрим соединение с кафкой и топиками 
# [2025/01/05 09:21:56] [ info] [output:kafka:kafka.0] brokers='kafka:9092' topics='kube'
# [2025/01/05 09:21:56] [ info] [output:kafka:kafka.1] brokers='kafka:9092' topics='host'
kafka     - наличие сообщений в топиках


```



