##### Добавление метрик из файла

Создадим файл, который будет содержать метрики.
```bash 
mkdir /tmp/node_exporter/
cat <<EOF > /tmp/node_exporter/node_exporter_custom_metric.prom
#TYPE slurm_demo_metric counter
slurm_demo_metric 100
EOF
```
Настраиваем Node Exporter для чтения метрик из файла
В указанном каталоге Node Exporter читает все файлы по маске *.prom
```bash 

cat <<EOF > /etc/sysconfig/node_exporter
OPTIONS="--collector.textfile.directory=/tmp/node_exporter"
EOF
```

```bash
systemctl restart node_exporter


curl -si http://localhost:9100/metrics | grep slurm

## HELP slurm_demo_metric Metric read from /tmp/node_exporter/node_exporter_custom_metric.prom
## TYPE slurm_demo_metric counter
# slurm_demo_metric 100

```

