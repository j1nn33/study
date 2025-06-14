##### How to work grok

https://habr.com/ru/articles/509632/
https://www.javainuse.com/grok

```bash
кусок лога 
localhost GET /v2/applink/5c2f4bb3e9fda1234edc64d 400 46ms 5bc6e716b5d6cb35fc9687c0

хотим 
Структурированный вид наших данных

​ localhost == environment
​ GET == method
​ /v2/applink/5c2f4bb3e9fda1234edc64d == url
​ 400 == response_status
​ 46ms == response_time
​ 5bc6e716b5d6cb35fc9687c0 == user_id

-----------
1 - каждая часть разделена пробелом 
2 - синтаксис шаблонов Grok       %{pattern:Name_of_the_field}  Name_of_the_field между названиями полей нет пробелов


Полученный шаблон 
%{WORD:environment} %{WORD:method} %{URIPATH:url} %{NUMBER:response_status} %{WORD:response_time} %{USERNAME:user_id}

```

######## патерны берем тут

https://github.com/elastic/logstash/blob/v1.4.2/patterns/grok-patterns
https://www.alibabacloud.com/help/en/sls/user-guide/grok-patterns
  

####### Понимание шаблонов 
https://edgedelta.com/company/blog/what-are-grok-patterns

```bash
^   для обозначения начала шаблона    ^%{IP:ip}
– –  чтобы Grok игнорировал их: ^%{IP:ip} – –
^%{IP:ip} – – [%{HTTPDATE:timestamp}]

"%{WORD:verb}  метод WORD для таких глаголов, как WRITE, + игнорировать кавычки

%{DATA:request}  Метод DATA извлекает такие запросы, как /topic/technical HTTP/1.1. Чтобы указать функции DATA, где остановиться, можно использовать кавычки в качестве знака остановки: %{DATA:request}

Пример 
^%{IP:ip} – – [%{HTTPDATE:timestamp}] "%{WORD:verb} %{DATA:request}" %{NUMBER:status} %{NUMBER:bytes} "%{DATA:referrer}"
```