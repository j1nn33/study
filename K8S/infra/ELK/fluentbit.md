см видео 

fluentbit   - собирает логи с каждой ноды каластера


/var/log/containers/<name_pod>_<name_namespace>_*.log
/var/log/containers/*_kube-system_*.log


версию приклада в файле берем из docker hub /fluent/fluent-bit 

- image: fluent/fluent-bit:3.2.2-amd64
