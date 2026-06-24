#### Модификаторы labels
```
Для модификации labels в Prometheus есть 2 варианта: 
    - relabel_configs        производит все модификации до scraping
    - metric_relabel_configs производит изменения после scraping, но перед сохранением в базу.
       обычно используется в двух случаях: когда надо удалить метрику или переименовать ее.
       metric_relabel_configs не применяется к автоматически генерируемым метрикам, таким как up.
```
#### Модификаторы
```
список действий, которые можно производить с метриками. Для metric_relabel_configs и relabel_configs они одинаковы.
```

###### Labels action
```
С помощью action можно задавать правила scraping. Возможны значения: keep или drop.
- keep, будет производиться scraping метрик только с этим labels. 
- drop, то метрики с этим labels не будут сохраняться.

Пример. В этом случае будет производиться scraping только метрик, которые имеют 
label  _meta_openstack_tag равный db:
```
```yaml

scrape_configs:
  - job_name: 'openstack'
    openstack_sd_configs:
    - identity_endpoint: https://api.openstack.local/identity/v3
        port: 9100
        domain_name: '<domain_name>'
        username: '<user_name>' 
        project_name: '<project_name>' 
        password: '<password>'
        role: 'instance'
        region: '<region>' 
        refresh_interval: 30s
    relabel_configs:
    - source_labels: [_meta_openstack_tag]
      regex: db
       action: keep
```

```
В этом случае будет производиться scraping метрик, у которых значение labels
_meta_openstack_tag равно: front, либо db, либо back не будут сохранены
```
```yaml

scrape_configs:
  - job_name: 'openstack'
    openstack_sd_configs:
    - identity_endpoint: https://api.openstack.local/identity/v3
        port: 9100
        domain_name: '<domain_name>'
        username: '<user_name>' 
        project_name: '<project_name>' 
        password: '<password>'
        role: 'instance'
        region: '<region>' 
        refresh_interval: 30s
    relabel_configs:
    - source_labels: [_meta_openstack_tag]
      regex: front|db|back
       action: drop
```

```
Важный момент: все метки, начинающиеся с _ , в конце обработки отбрасываются и
не попадают в target labels

```

###### Labels replace
```
есть несколько команд, работающих над проектом, они могут использовать разное именование одних и тех же меток. 
В этом случае можно привести все к единому виду

Если метрика имеет метку team со значением developing, то в результате
преобразования значение team будет заменено на develop.
```

```yaml
relabel_configs:
  - source_labels: [team]
    regex: '(.*)ing'
    replacement: '${1}'
    target_label: team
    action: replace

```

###### Labels labelmap
```
Label map позволяет использовать имена source labels как имена для target labels.
Именем для новой метки будет часть, удовлетворяющая регулярному выражению.
Например, если есть source label __meta_filepath, то конфигурация:
добавит target label filepath со значением равным значению __meta_filepath.
```
```yaml
relabel_configs:
  - regex: __meta_(filepath)
    replacement: '${1}'
    action: labelmap
```

###### Labels list
```
Некоторые SD не имеют значений key:value, вместо которых у них список. Вы можете за
счет регулярного выражения выделить нужное значение. В этом примере, если в списке
тэгов consul присутствует один из тэгов с именем: prod|staging|dev, то имя этого тэга
сохранится как значение label env.
```
```yaml
relabel_configs:
  - source_labels: [__meta_consul_tag]
    regex: '.*,(prod|staging|dev),.*'
    target_label: env
```

###### Labels labeldrop
```
Все метки, удовлетворяющие регулярному выражению, будут удалены.
```
```yaml
relabel_configs:
  - regex: sd
    action: labeldrop
```

###### Labels labelkeep
```
Все метки, не удовлетворяющие регулярному выражению, будут удалены.
Этот модификатор необходимо использовать с осторожностью, так как все
служебные метки(относятся к source labels) тоже удаляются. В примере выше будут
удалены, в частности, такие метки, как: __address__ и __scheme__, что сделает
невозможным проведение scraping с exporter
```
```yaml
relabel_configs:
  - regex: sd
    action: labelkeep
```
