#### Пример
```
   Описание
   Создание chart
   Chart.yaml
   templates
   Файл _helpers.tpl
   - реадктирвоание deployment
   -   Встроенные объекты
   -   Labels
   -   Annotations
   Проверка работы шаблонов
   Переопределение параметров по умолчанию
   Работа с приложением
   Раздел spec deployment.
   Спецификация контейнера.
   -  Container
   -  Пробы
   -  Ресурсы
    Service
   Ingress
   NOTE.txt
   VARIANT 1
   VARIANT 2
   Удалить лишнее.
   Добавить нужное.
   Создать файл чарта.
   Опубликовать чарт.
```
###### Описание
```
Обчающий пример 

Приложение - openresty, которое запускаем в кластере kubernetes. 
Файлы приложения 
./K8S/helm/teach_example/base-application

На основе этих манифестов создается helm chart 
```
###### Создание chart
```
mkdir teach_example_chart
cd teach_example_chart/

# создание чарта openresty-art
helm create openresty-art

ls -la
# - charts        - использовать не будетм
# - templates     - находятся темпленты 
# - Chart.yaml    - оснвной конфигурационный чарт
# - values.yaml   - конфигурационные параметры по умолчанию чарта

```
##### Chart.yaml
```
параметры которые обязательны в Chart.yaml
```
```yaml
apiVersion: v2                                    # версия apiVersion
name: openresty-art                               # имя чарта 
description: A Helm teach example openreasty art  # описание 
type: application                                 # application\Library
                                                  # application - приложение 
                                                  # Library     - бибилиотека которая включается в другой чарт
version: 0.1.0                                    # версия чарта 
appVersion: "1.19.9.1-centos-rpm"                 # версия приложения которое находится внутри чарта 
kubeVersion: ">= 1.19.0"                          #
```
##### templates
```
параметры которые обязательны в Chart.yaml

Из директории templates удаляем не нужные файлы.
cd openresty-art/templates
rm -rf {tests,hpa.yaml,serviceaccount.yaml}

Переименовываем и переносим автоматически созданные файлы. Мы их потом удалим, но по ходу правки будем заимствовать из них некоторые шаблоны.

./K8S/helm/teach_example_chart

mkdir ./K8S/helm/teach_example_chart/old-templates
mv deployment.yaml ../../old-templates/deployment-orig.yaml 
mv service.yaml ../../old-templates/service-orig.yaml 
mv ingress.yaml ../../old-templates/ingress-orig.yaml

Скопируем манифесты нашего приложения в директорию templates
cp ./K8S/helm/teach_example_chart/base-application/* .

далее пойдет процесс шаблонизации этих файлов 
```
##### Файл _helpers.tpl
```
# Команда helm create создала шаблон _helpers.tpl, в который поместила вспомогательные (условно) функции. 
# Эти функции можем использовать в шаблонах. Что -то типа библиотеки шаблонов 
{{ }}  # - шаблон

{{-    # удаление пробелов в начале
-}}    # удаление пробелов в конце 

# define определяет вложенные именнованые шаблоны.
{{- define "openresty-art.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

# В дальнейшем в любых файлах нашего чарта мы можем обратиться к такому шаблону при помощи include.
# Например:
# Тут будет что то вставлено: {{ include "openresty-art.chart" . }}

# После обработки, в данном месте будет подставлено содержимое вложенного шаблона:

# Тут будет что то вставлено: {{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}

# Итого в файле определено:

openresty-art.name                 - имя чарта.
openresty-art.fullname             - имя приложения.
openresty-art.chart                - имя чарта с версией.
openresty-art.labels               - общий набор labels, которые можно подставлять в metadata манифестов.
openresty-art.selectorLabels       -  набор labels, которые можно использовать в селекторах. Например, в селекторах service.
openresty-art.serviceAccountName   - имя SeviceAccount. При условии, что оно определено в файле values.

```
##### - реадктирвоание deployment
```

# - исходник (оригинал который не helm)           ./K8S/helm/teach_example/base-application/deployment.yaml
# - образец  (оригинал который сгенерирован helm) ./K8S/helm/teach_example_chart/old-templates/deployment-orig.yaml
# - целевой  (итоговый файл helm)                 ./K8S/helm/teach_example_chart/openresty-art/templates/deployment.yaml
# - бибилотека шаблонов                           ./K8S/helm/teach_example_chart/openresty-art/templates/_helpers.tpl

# методика
# целевой получается в реузльтате корректировки исхдоника
# в исходнике заменяются сторки (беруться из образца и несколько модифицируются)

name: {{ include "openresty-art.fullname" . }} 
# помощи include берется из бибилотека шаблонов

{{- define "openresty-art.fullname" -}}
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

# разбор выражение будет ниже
```
##### Встроенные объекты
[Документация](https://helm.sh/docs/chart_template_guide/builtin_objects/)
```
# Release       - описывает сам релиз.
# Values        - значение из файла values.yaml (параметры по умолчанию).
# Files         - доступ к файлам в чарте (кроме файлов шаблонов).
# Capabilities  - информация о кластере kubernetes.
# Template      - информация о текущем файле шаблона.

{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}

# Оператор if проверяет pipeline. Если pipeline возвращает 0 или пустой объект - тогда условие = false. Иначе true.
# В нашем случае используется встроенный объект Values. В файле values.yaml 
# ./K8S/helm/teach_example_chart/openresty-art/values.yaml
# берется параметр объекта fullnameOverride. Ниже выдержка из файла values.yaml
# nameOverride: ""
# fullnameOverride: ""

# По итогу если fullnameOverride в values.yaml - определено 
# то истина (в нашем случае не определено то ложь)
# иначе нет 

# trunc 63 обрезка строки от 0 до 63 включительно

# trimSuffix "-" обрезается суфиикс начиная с -
# пример fullnameOverride: "abs-0.1.0"
# то будет abs

{{- $name := default .Chart.Name .Values.nameOverride }}
# делаем временную переменную $name 
# функция default если .Values.nameOverride не определен, то используем .Chart.Name
# .Chart.Name берется из файла Chart.yaml   (./K8S/helm/teach_example_chart/openresty-art/Chart.yaml)
# name: openresty-art

{{- if contains $name .Release.Name }}
# contains проверяет, содержит ли вторая строка первую 
# входит ли $name в .Release.Name
# Если истина, шаблон выведет содержимое .Release.Name. Обрежет его на 63-м символе. Удалит суффикс.
# 
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
# вывод .Release.Name $name обрезанное до 63 с удаленным суффиксом


# по итогу правим в файлах 
# ./K8S/helm/teach_example_chart/openresty-art/templates/deployment.yaml
name: {{ include "openresty-art.fullname" . }}
# ./K8S/helm/teach_example_chart/openresty-art/templates/configmap-html.yaml
name: {{ include "openresty-art.fullname" . }}-html
# ./K8S/helm/teach_example_chart/openresty-art/templates/configmap-conf.yaml
name: {{ include "openresty-art.fullname" . }}-conf
# ./K8S/helm/teach_example_chart/openresty-art/templates/service.yaml
name: {{ include "openresty-art.fullname" . }}-srv
```
##### Labels
```
# deployment.yaml (./K8S/helm/teach_example_chart/openresty-art/templates/deployment.yaml)
labels:
   {{- include "openresty-art.labels" . | nindent 4 }}

# объект раздела metadata - это метки. Для их формирования в файле _helpers.tpl определен макрос.

{{- define "openresty-art.labels" -}}
helm.sh/chart: {{ include "openresty-art.chart" . }}
{{ include "openresty-art.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

# Разбор шаблона
#
# {{- define "openresty-art.labels" -}}
# helm.sh/chart: {{ include "openresty-art.chart" . }}
# подставлятеся имя чарта определено в _helpers.tpl - именнованый шабон
#      {{- define "openresty-art.chart" -}}
#      {{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
#      {{- end }}
#
# {{ include "openresty-art.selectorLabels" . }}
# подставлятеся openresty-art.selectorLabel определено в _helpers.tpl - именнованый шабон
#      {{- define "openresty-art.selectorLabels" -}}
#      app.kubernetes.io/name: {{ include "openresty-art.name" . }}   # имя 
#      app.kubernetes.io/instance: {{ .Release.Name }}                # Release.Name
#      {{- end }}

# {{- if .Chart.AppVersion }}
# app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}          # берется из файла Chart.yaml
# {{- end }}
# app.kubernetes.io/managed-by: {{ .Release.Service }}
# {{- end }}

# | nindent 4 }} - формирует отступы 4 символа вначале строки 

# по итогу правим в файлах 
# ./K8S/helm/teach_example_chart/openresty-art/templates/deployment.yaml
{{- include "openresty-art.labels" . | nindent 4 }}
# ./K8S/helm/teach_example_chart/openresty-art/templates/configmap-conf.yaml
{{- include "openresty-art.labels" . | nindent 4 }}
# ./K8S/helm/teach_example_chart/openresty-art/templates/service.yaml
{{- include "openresty-art.labels" . | nindent 4 }}

```
##### Annotations
```
# Предполагается использовать reloader.stakater.com, который перезапускает приложение, в случае изменения ConfigMap или Secret. 
# Но, есть вероятность, что в кластере это приложение не установлено. Эту возможность надо предусмотреть.

# В файле values.yaml добавим объект application, в который мы будем помещать все параметры деплоймента. 
# Там же добавим объект reloader и присвоим ему значение по умолчанию false.

application:
  reloader: false

# те когда chart будте ставиться
# при reloader: false 

# строк в deployment.yaml (./K8S/helm/teach_example_chart/openresty-art/templates/deployment.yaml)

# НЕ БУДЕТ, они появятся при reloader: true
  {{- if .Values.application.reloader }}
  annotations:
    reloader.stakater.com/auto: "true"
    configmap.reloader.stakater.com/reload: {{ include "openresty-art.fullname" . }}-conf,{{ include "openresty-art.fullname" . }}-html
  {{- end }}
```
##### Проверка работы шаблонов
##### Переопределение параметров по умолчанию
##### Работа с приложением
##### Раздел spec deployment.
##### Спецификация контейнера.
###### -  Container
###### -  Пробы
###### -  Ресурсы
#####  Service
##### Ingress
##### NOTE.txt
##### VARIANT 1
##### VARIANT 2
##### Удалить лишнее.
##### Добавить нужное.
##### Создать файл чарта.
##### Опубликовать чарт.
###### Описание