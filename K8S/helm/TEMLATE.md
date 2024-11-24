##### TEMPLATE MAN
```
{{ }} - шаблон

{{/*
comment
*/}}
```
{{-    удаление пробелов в начале
-}}    удаление пробелов в конце 

шаблон     {{ "abc" }}  xx {{ "abc" }}
результат  abc  xx abc

шаблон     {{ "abc" -}}  xx {{- "abc" }}
результат  abcxxabc

Оператор if проверяет pipeline. Если pipeline возвращает 0 или пустой объект - тогда условие = false. Иначе true.
если значнеие в  файле values.yaml 
берется параметр объекта fullnameOverride. 
```
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
trunc 63     обрезка строки от 0 до 63 включительно
trimSuffix   "-" обрезается суфиикс начиная с -
quote        Она помещает строку в двойные кавычки.
```
# пример 
fullnameOverride: "abs-0.1.0"
# то будет abs
{{- include "openresty-art.labels" . | nindent 4 }}
# | nindent 4 }} - формирует отступы 4 символа вначале строки 
```