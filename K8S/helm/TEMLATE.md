##### TEMPLATE MAN
```
- удаление пробелов
- if
- other
   - trunc 63      обрезка строки от 0 до 63 включительно
   - trimSuffix    "-" обрезается суфиикс начиная с -
   - quote         Она помещает строку в двойные кавычки.
- Пространство имен
- with
```
{{ }} - шаблон

```yaml
{{/*
comment
*/}}
```
###### удаление пробелов
{{-    удаление пробелов в начале
-}}    удаление пробелов в конце 

шаблон     {{ "abc" }}  xx {{ "abc" }}
результат  abc  xx abc

шаблон     {{ "abc" -}}  xx {{- "abc" }}
результат  abcxxabc

###### if
Оператор if проверяет pipeline. Если pipeline возвращает 0 или пустой объект - тогда условие = false. Иначе true.
если значнеие в  файле values.yaml 
берется параметр объекта fullnameOverride. 
```yaml
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}   
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}
```
###### other
trunc 63     обрезка строки от 0 до 63 включительно

trimSuffix   "-" обрезается суфиикс начиная с -
пример: 
fullnameOverride: "abs-0.1.0"
то будет abs
```yaml
{{- include "openresty-art.labels" . | nindent 4 }}
```
nindent 4 }} - формирует отступы 4 символа вначале строки 

quote         Она помещает строку в двойные кавычки.
###### Пространство имен 
Когда мы пишем путь к переменным, мы его обычно начинаем с символа точка (вершина пространства имён). 
Например: .Values.application.podAnnotations. Если предполагается, что в указанном узле много переменных,
то можно "переместить" точку в конец podAnnotations.
###### with
структура управления with, которая устанавливает область видимости переменных.
т.е. смещение пространства имен
Затем при помощи toYaml перенесём все как есть в итоговый манифест. (которые находятся в простренстве .Values.application.podAnnotations) 
тк with мы уже сместили пространство имен 

Если podAnnotations не пустое, то выполняется то что внизу 
```yaml
      {{- with .Values.application.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```

Предполагается, что my-values.yaml мы будем явно описывать аннотации. Например, вот так:
```yaml
application:
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/path: "/metrics"
    prometheus.io/port: "80"
```

