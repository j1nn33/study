package main

import (
	"net/http"
	"time"

	log "github.com/sirupsen/logrus"
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
