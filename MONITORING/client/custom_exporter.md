##### Общие рекомендации по написанию exporter
```
1. Выбор имени для метрик:

   -  Имена метрик должны быть в нижнем регистре.

   -  Для именования допускаются только символы: [a-zA-Z0-9:_].

   -  _sum, _count, _bucket и _total суффиксы, которые используются для
      Summaries, Histograms и Counters. В других случаях использовать их не стоит.

   -  process_ и scrape_ являются зарезервированными префиксами.

   -  Из названия метрики должно быть понятно, что эта метрика собирает.

   -  В названии метрики должны содержаться единицы измерения.


 Пример плохого именования
 http_request_duration    
 
 Из названия не ясны ни единицы, в которых производится измерение, ни к какому
 приложению метрика относится.
 
 Пример хорошего именования этой же метрики:
 nginx_http_request_duration_seconds_bucket
 
 
 Если есть число удачных запросов, число неудачных запросов и общее количество запросов, 
 то лучше сделать 2 метрики: число удачных запросов и общее число запросов. 
 В этом случае число неудачных запросов легко обработать.


2. Выбор labels:
  
   -  Ряд слов, использовать которые в имени метки не запрещено, но и не рекомендовано: 
       region, zone, cluster, az, datacenter, customer, dc, owner, stage, 
       service, environment, job, instance.

   -  Метку le стоит использовать только с Histograms, а метку quantile стоит
      использовать только с Summaries.

   -  Метки необходимо выбирать таким образом, чтобы сумма значений метрики
      имела значение. Например, read/write показатели лучше хранить как отдельные
      метрики, а не разделять с использованием labels.


3. Рекомендации по написанию exporters:

  -  Получение данных должно производиться, только когда Prometheus производит scraping.
  -  Не надо выставлять временные метки для метрик, это задача Prometheus.
  -  Выбирать порт для exporter стоит с учетом уже занятых портов. 
     Список уже использованных портов размещен на https://github.com/prometheus/prometheus/wiki/Default-port-allocations.

```
#### Пример exporter на языке go

```
Exporter написан на языке go. Для реализации exporter используются готовые библиотеки 
prometheus. Exporter возвращает стандартные метрики, связанные с потреблением ресурсов 
самим exporter; данные метрики являются частью функционала библиотеки. Также присутствует
собственная метка с типом данных Counter. Данная метрика увеличивает свое значение каждые 2 секунды.

```

```bash
vim slurm_exporter.go
```
```go

package main

import (
	"net/http"
	"time"

	log "github.com/Sirupsen/logrus"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)


func recordMetrics() {
	go func() {
		for {
			opsProcessed.Inc()
			time.Sleep(2 * time.Second)
		}
	}()
}

var (
	opsProcessed = promauto.NewCounter(prometheus.CounterOpts{
		Name: "slurm_example_exporter_processed_ops_total",
		Help: "The total number of processed events",
	})
)

func main() {
	recordMetrics()
	http.Handle("/metrics", promhttp.Handler())
	log.Info("Beginning to serve on port :2112")
	log.Fatal(http.ListenAndServe(":2112", nil))
}

```

```bash 
# Устанавливаем go на сервер
yum install -y go

# Устанавливаем необходимые зависимости:

go mod init custom-exporter

go get -d -u github.com/prometheus/client_golang/prometheus
go get -d -u github.com/sirupsen/logrus  
go mod tidy
go mod verify
# Первая зависимость – это библиотека prometheus. 
# Вторая библиотека – для реализации логирования.

#  Запускаем exporter:
go run slurm_exporter.go


# Проверка работоспособности.
# Откройте еще одно подключение к серверу monitoring и выполните в новой консоли:
curl http://localhost:2112/metrics

# В результате вы должны получить полный список метрик, который предоставляет exporter


# HELP slurm_example_exporter_processed_ops_total The total number of processed events
# TYPE slurm_example_exporter_processed_ops_total counter
slurm_example_exporter_processed_ops_total 8

```