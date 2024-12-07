#### Пример
```
   Описание
   Создание chart
   Chart.yaml
   templates
   my-values.yaml
   Файл _helpers.tpl
   реадктирвоание deployment
  -   Встроенные объекты
  -   Labels
  -   Annotations
   Проверка работы шаблонов
   Переопределение параметров по умолчанию
   Работа с приложением
   Раздел spec deployment
   Аннотации пода
   Спецификация контейнера
   -  Container
   -  Пробы
   -  Ресурсы
   реадктирвоание Service
   реадктирвоание Ingress
   реадктирвоание NOTE.txt
   ConfigMap
    VARIANT 1
    VARIANT 2
   Удалить лишнее
   Добавить нужное
   Создать файл чарта
   Опубликовать чарт
```
###### Описание
```
Обчающий пример 

Приложение - openresty, которое запускаем в кластере kubernetes. 
Файлы приложения 
./K8S/helm/teach_example_chart/base-application

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
##### my-values.yaml
```
используется для задания своих параметров и переопределениая параметров по умолчанию
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
##### реадктирвоание deployment
```

# - исходник (оригинал который не helm)           ./K8S/helm/teach_example_chart/base-application/deployment.yaml
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
name: {{ include "openresty-art.fullname" . }}-svc
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
```
# перейдём в директорию, в которой находится наш чарт.

helm template <release_name> ./openresty-art --debug > app.yaml

# Эта команда заставляет helm преобразовать шаблоны и выдать на стандартный вывод итоговый набор манифестов.
# Дополнительный парамер --debug, заставляет программу выводить отладочную информацию, которая будет полезной в случае обнаружения ошибок в шаблонах.

helm template app ./openresty-art --debug > app.yaml

# В результате формируется файл с манифестами app.yaml. Откройте его и посмотрите начало определения деплоймента.


```
##### Переопределение параметров по умолчанию
```
# Настройки по умолчанию
values.yaml (./K8S/helm/teach_example_chart/openresty-art/values.yaml)

# Для переопределения настроек по умолчанию используется 2 спосба 
# 1 При помощи параметра --set
helm template app ./openresty-art --set "application.reloader=true" --debug > app.yaml

# 2 Создав и применив собственный yaml файл с переопределёнными параметрами.

# Файл my-values.yaml
```
```yaml
fullnameOverride: "art"

application:
  reloader: true
```
```
helm template app ./openresty-art -f my-values.yaml > app.yaml
helm template app ./openresty-art -f ./openresty-art/my-values.yaml > app.yaml

```
##### Работа с приложением
```
Установим приложение.

# helm install app ./openresty-art --namespace app -f ./openresty-art/my-values.yaml
# ./study/K8S/helm/teach_example_chart/openresty-art/my-values.yaml
helm install app ./openresty-art -f ./openresty-art/my-values.yaml

# helm list --namespace app
helm list
# NAME    NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
# app     default         1               2024-10-09 12:11:02.053952538 +0300 MSK deployed        openresty-art-0.1.0     1.19.9.1-centos-rpm

# Удалим приложение.
# helm uninstall <relese_name>
# helm uninstall app --namespace app
helm uninstall app
```

##### Раздел spec deployment.
```
В values.yaml переносим replicaCount в раздел application и добавим revisionHistoryLimit
```
```yaml
application:
  reloader: false
  replicaCount: 1
  revisionHistoryLimit: 3
```  
В шаблоне deployment.yaml добавляем соответствующие шаблоны.
```yaml
spec:
  replicas: {{ .Values.application.replicaCount }}
  revisionHistoryLimit: {{ .Values.application.revisionHistoryLimit }}
```
изменим раздел selector.matchLabels. Тут просто подставим готовый именованный шаблон, 
при помощи которого определяем labels селектора подов. 
берем из сгенерированного файла (при создании helm chart)
./K8S/helm/teach_example_chart/old-templates/deployment-orig.yaml
 {{- include "openresty-art.selectorLabels" . | nindent 6 }}
ссылается на _helpers.tpl

Аналогичный шаблон, подставляем в разделе template.metadata.labels.
```yaml
  selector:
    matchLabels:
      {{- include "openresty-art.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      labels:
        {{- include "openresty-art.selectorLabels" . | nindent 8 }}
```
#####  Аннотации пода
```
Аннотации пода нам могут потребоваться например, для сбора метрик. 
Для данного случая не актуально тк этот образ openresty такие метрики отдавать не умеет

В values.yaml переносим podAnnotations в раздел application. 
И Оставляем его значение пустым. Т.е. по умолчанию аннотаций нет.
```
```yaml
application:
  podAnnotations: {}
```

В шаблоне deployment.yaml в template.metadata добавляем шаблон.
```yaml
template:
    metadata:
      {{- with .Values.application.podAnnotations }}
      annotations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```
В этом шаблоне мы применяем структуру управления with, которая устанавливает область видимости переменных.
т.е. смещение пространства имен

Когда мы пишем путь к переменным, мы его обычно начинаем с символа точка (вершина пространства имён). Например: .Values.application.podAnnotations. Если предполагается, что в указанном узле много переменных, то можно "переместить" точку в конец podAnnotations.

Затем при помощи toYaml перенесём все как есть в итоговый манифест. (которые находятся в простренстве .Values.application.podAnnotations) 
тк with мы уже сместили пространство имен 
Т.е. не будем разрешать остальные переменные и их значения. Просто скопируем.
напирмет будет то что снизу 
  prometheus.io/scrape: "true" и тд

Предполагается, что my-values.yaml мы будем явно описывать аннотации. Например, вот так:
Как работает пример:
указыавем в файле my-values.yaml (файл который используем для переопределиня параметров)
./study/K8S/helm/teach_example_chart/openresty-art/my-values.yaml
значения поедут из файла my-values.yaml

```yaml
application:
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/path: "/metrics"
    prometheus.io/port: "80"
```
в deployment получаем 

helm template app ./openresty-art -f my-values.yaml > app.yaml
```yaml
spec:
  replicas: 1
  revisionHistoryLimit: 3
  selector:
    matchLabels:
      app.kubernetes.io/name: openresty-art
      app.kubernetes.io/instance: app
  template:
    metadata:
      labels:
        app.kubernetes.io/name: openresty-art
        app.kubernetes.io/instance: app
      annotations:
        prometheus.io/path: /metrics
        prometheus.io/port: "80"
        prometheus.io/scrape: "true"

```
##### Спецификация контейнера
```
spec.template.spec.containers.

imagePullSecrets
добавим возможность указать imagePullSecrets.

В values.yaml переносим в раздел application imagePullSecrets. По умолчанию, массив пустой.
```
```yaml
application:
  imagePullSecrets: []
```
В шаблоне deployment.yaml добавим следующую конструкцию. из файла 
study/K8S/helm/teach_example_chart/old-templates/deployment-orig.yaml
с учетом того что в файле values.yaml imagePullSecrets в разделе application
поэтом будет Values.application.imagePullSecrets 
вместо       Values.imagePullSecrets

```yaml
    spec:
      {{- with .Values.application.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
```
При помощи with меняем область видимости. И при помощи toYaml преобразуем все что там есть в yaml. По умолчанию у нас там пустой массив. Поэтому в итоговый манифест не подставиться.

Но если в my-values.yaml мы добавим указание имени сикрета, то секция будет сформирована.
```yaml
application:
  reloader: true
  podAnnotations:
    prometheus.io/scrape: "true"
    prometheus.io/path: "/metrics"
    prometheus.io/port: "80"
  imagePullSecrets:
    - name: MypullSecretName
```
```
Проверим
helm template app ./openresty-art -f my-values.yaml > app.yaml
    spec:
      imagePullSecrets:
        - name: pullSecretName
Удалим imagePullSecrets из my-values.yaml, поскольку мы предполагаем использование публичного docker registry.

```
###### -  Container
```
В первую очередь определим: name, image и imagePullPolicy. 
(имена подов, image и откуда забирать imagePullPolicy)

образец берем из ./study/K8S/helm/teach_example_chart/old-templates/deployment-orig.yaml

имя пода соотаветсвует имени чарта {{ .Chart.Name }}
или {{ include "openresty-art.fullname" . }}

image
образец использует значения сгенерированные автоматикой в values.yaml
image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
image: "{{ .Values.application.image.repository }}:{{ .Values.application.image.tag | default "centos-rpm" }}"

В values.yaml добавим в раздел application значения по умолчанию:
```
```yaml
application:
  image:
    repository: openresty/openresty
    tag: "centos-rpm"
    pullPolicy: IfNotPresent
```
```
В deployment.yaml добавим соответствующие шаблоны.
```
```yaml
      containers:
        - name: {{ include "openresty-art.fullname" . }}
          image: "{{ .Values.application.image.repository }}:{{ .Values.application.image.tag | default "centos-rpm" }}"
          imagePullPolicy: {{ .Values.application.image.pullPolicy }}
```
```          
Из интересного тут только установка значения по умолчанию в шаблоне {{ .Values.application.image.tag | default "centos-rpm" }}

Если tag не определен, будет подставлено значение "centos-rpm".

Проконтролируем правильность создания шаблона.
helm template app ./openresty-art -f my-values.yaml > app.yaml
```
###### -  Пробы
```
В созданном helm create шаблоне пробы не обёрнуты в шаблон.
B values.yaml, раздел application добавим следующие строки:
```
```yaml
application:
  probe:
    readinessProbe:
      httpGet:
        path: /
        port: http
    livenessProbe:
      httpGet:
        path: /
        port: http
```
В deployment.yaml вместо определения проб:
```
```yaml
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.application.image.repository }}:{{ .Values.application.image.tag | default "centos-rpm" }}"
          imagePullPolicy: {{ .Values.application.image.pullPolicy }}
          ports:
            - containerPort: 80
              name: http
          {{- with .Values.application.probe }}
          {{- toYaml . | nindent 10 }}
          {{- end }}
```
В my-values.yaml добавим немного изменённое определение проб.
```yaml
  probe:
    readinessProbe:
      httpGet:
        path: /index.html
        port: http
      initialDelaySeconds: 5
      periodSeconds: 15
    livenessProbe:
      httpGet:
        path: /index.html
        port: http
      initialDelaySeconds: 5
      periodSeconds: 15
      timeoutSeconds: 5
```      
Проконтролируем правильность генерации проб.
helm template app ./openresty-art -f my-values.yaml > app.yaml

###### -  Ресурсы
```
В файле values.yaml переносим resources в раздел application.

```yaml
application:
  resources: {}
```  
По умолчанию у нас нет ограничений.

В файле deployment.yaml добавим соответствующий шаблон.
```yaml
      containers:

          {{- with .Values.application.resources }}
          resources:
            {{- toYaml . | nindent 12 }}
          {{- end }}
```          
Проверим, что по умолчанию ресурсы не добавляются в манифест.
```
helm template app ./openresty-art > app.yaml
Добавим в файл my-values.yaml определение ресурсов:
```
```yaml
application:
  resources:
    limits:
      cpu: "0.2"
      memory: "400Mi"
    requests:
      cpu: "0.1"
      memory: "200Mi"
```
```
Проверим, что ресурсы корректно подставляются.
```
#####  Service
```
# - исходник (оригинал который не helm)           ./K8S/helm/teach_example_chart/base-application/service.yaml
# - образец  (оригинал который сгенерирован helm) ./K8S/helm/teach_example_chart/old-templates/service-orig.yaml
# - целевой  (итоговый файл helm)                 ./K8S/helm/teach_example_chart/openresty-art/templates/service.yaml

В файле values.yaml переносим (добавляем) строки:
```
```yaml
service:
  # Service type: ClusterIP or NodePort (используем только один из двух типов сервисов)
  type: ClusterIP
  port: 80
  # Если сервис типа NodePort
  nodePort: ""
  # Если необходимо, определите имя порта
  name: ""
```  
Предполагается, что наш чарт будет поддерживать только два типа сервисов: CluserIP (по умолчанию) и NodePort.
В фале service.yaml добавляем шаблон.
```yaml
spec:
  type: {{ .Values.service.type }}
  ports:
    - port: {{ .Values.service.port }}
```    
Так же нам необходимо отработать ситуацию, когда сервиса типа NodePort. В этом случае следует определить параметр nodePort, в случае, если он определён. В этом нам поможет следующая конструкция:
```yaml
      {{- if and (eq .Values.service.type "NodePort") .Values.service.nodePort }}
      nodePort: {{ .Values.service.nodePort }}
      {{- end }}
```      
В качестве значения оператору if передаётся функция and. Которая проверяет истинность двух значений:

eq .Values.service.type "NodePort" - истина, если type равен NodePort.
.Values.service.nodePort - истина, если значение определено.
Если оба значения истина, то будет подставлен параметр nodePort.

Так же добавим формирование имени порта:
```yaml
      {{- if .Values.service.name }}
      name: {{ .Values.service.name }}
      {{- end }}
```      
Добавим в файл my-values.yaml следубщие строки:
```yaml
service:
  type: NodePort
  nodePort: 31002
  name: proxy
```  
selector берем из deployment
```yaml
  selector:
     {{- include "openresty-art.selectorLabels" . | nindent 4 }}
```
```
Проверим создание шаблона.
helm template app ./openresty-art/ -f my-values.yaml > app.yaml

```
##### Ingress
```
# - исходник (оригинал который не helm)           ./K8S/helm/teach_example_chart/base-application/ingress.yaml
# - образец  (оригинал который сгенерирован helm) ./K8S/helm/teach_example_chart/old-templates/ingress-orig.yaml
# - целевой  (итоговый файл helm)                 ./K8S/helm/teach_example_chart/openresty-art/templates/ingress.yaml

Сначала в values.yaml перенесем всю секцию ingress. Так же скопируем эту секцию в my-values.yaml и немного её отредактируем.
на основении ./K8S/helm/teach_example_chart/base-application/ingress.yaml
```
```yaml
ingress:
  enabled: true
  className: "system-ingress"
  annotations:
    certmanager.k8s.io/cluster-issuer: monitoring-issuer
  hosts:
    - host: control1.kube.local
      paths:
        - path: /
          pathType: Prefix
  tls:
    - hosts:
        - application
      secretName: art-tls
```      
А затем просто скопируем ingress-orig.yaml в директорию templates и назовём его ingress.yaml. Т.е. просто удалим старый ingress.
Поскольку имя сервиса, относительно первоначально сгенерированного шаблона у нас изменено, добавим несколько дополнений/изменений в файле шаблона.

Правим 
{{- $fullName := include "openresty-art.fullname" . -}}
чтобы было как в service.yaml
name: {{ include "openresty-art.fullname" . }}-svc

После второй строки 
{{- $fullName := include "openresty-art.fullname" . -}}
добавим переменную:
{{- $svcName := printf "%s-%s" $fullName "svc" -}}

зедесь мы к $fullName добавляем -svc

В строках номер 53 и 57 заменим $fullName на $svcName.

Проверяем 

helm template app ./openresty-art/ -f my-values.yaml > app.yaml

Что бы разобраться в шаблоне, выпишем все используемые в нём, ещё не известный нам функции.

semverCompare - Семантическое сравнение двух строк. Два аргумента - строки в формате версии. Позволяет сравнить версии приложений.
hasKey - Возвращает истину, если данный словарь содержит данный ключ.
set - Добавляет в словарь новую пару ключ/значение.

```yaml
# Если .Values.ingress.className - определен и (версия kubernetis ) не выше 1.18-0
{{- if and .Values.ingress.className (not (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion)) }}
  # тогда ищем ключ Values.ingress.annotations равный kubernetes.io/ingress.class
  # если его нет то добавяленм ключ .Values.ingress.className = "kubernetes.io/ingress.class" в словарь .Values.ingress.annotations
  {{- if not (hasKey .Values.ingress.annotations "kubernetes.io/ingress.class") }}
  {{- $_ := set .Values.ingress.annotations "kubernetes.io/ingress.class" .Values.ingress.className}}
  {{- end }}
{{- end }}
# если semverCompare (версия kubernetis) >=1.19-0 то версия apiVersion
{{- if semverCompare ">=1.19-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1
{{- else if semverCompare ">=1.14-0" .Capabilities.KubeVersion.GitVersion -}}
apiVersion: networking.k8s.io/v1beta1
{{- else -}}
apiVersion: extensions/v1beta1
{{- end }}

spec:
  # если semverCompare (версия kubernetis) >=1.18-0 то подставляем ingressClassName:
  {{- if and .Values.ingress.className (semverCompare ">=1.18-0" .Capabilities.KubeVersion.GitVersion) }}
  ingressClassName: {{ .Values.ingress.className }}
  {{- end }}
  # если определена tls то пробегаемся по элементам массива range
  {{- if .Values.ingress.tls }}
  tls:
    {{- range .Values.ingress.tls }}
    - hosts:
        {{- range .hosts }}
        - {{ . | quote }}
        {{- end }}
      secretName: {{ .secretName }}
    {{- end }}
  {{- end }}
  rules:
    # в зависимости от версии kubernetis пробегаемся по элементам массива range внизу пример элемента массива
    # - host: control1.kube.local
    #   http:
    #     paths:
    #       - path: /
    #         pathType: Prefix
    {{- range .Values.ingress.hosts }}
    # в массиве есть параметр host который помещаем в двойные кавычки 
    - host: {{ .host | quote }}
      http:
        paths:
          {{- range .paths }}
          - path: {{ .path }}
            {{- if and .pathType (semverCompare ">=1.18-0" $.Capabilities.KubeVersion.GitVersion) }}
            pathType: {{ .pathType }}
            {{- end }}
            backend:
              {{- if semverCompare ">=1.19-0" $.Capabilities.KubeVersion.GitVersion }}
              # генерация значений в зависимости от версии kubernetis
              service:
                name: {{ $svcName }}
                port:
                  number: {{ $svcPort }}
              {{- else }}
              # генерация значений в зависимости от версии kubernetis
              serviceName: {{ $svcName }}
              servicePort: {{ $svcPort }}
              {{- end }}
          {{- end }}
    {{- end }}
{{- end }}
 
```
##### NOTE.txt
```
Содержимое файла NOTE.txt выводится на стандартный вывод после установки или обновления чарта (helm install или helm upgrade).
```
```yaml
1. Get the application URL by running these commands:
# если ingress включен то 
{{- if .Values.ingress.enabled }}
{{- range $host := .Values.ingress.hosts }}
  {{- range .paths }}
  # информация к каким хостам подключаемся 
  http{{ if $.Values.ingress.tls }}s{{ end }}://{{ $host.host }}{{ .path }}
  {{- end }}
{{- end }}
# иначе идет проверка на тип сервиса NodePort
{{- else if contains "NodePort" .Values.service.type }}
  export NODE_PORT=$(kubectl get --namespace {{ .Release.Namespace }} -o jsonpath="{.spec.ports[0].nodePort}" services {{ include "openresty-art.fullname" . }})
  export NODE_IP=$(kubectl get nodes --namespace {{ .Release.Namespace }} -o jsonpath="{.items[0].status.addresses[0].address}")
  echo http://$NODE_IP:$NODE_PORT
# иначе идет проверка на тип сервиса LoadBalancer  
{{- else if contains "LoadBalancer" .Values.service.type }}
     NOTE: It may take a few minutes for the LoadBalancer IP to be available.
           You can watch its status by running 'kubectl get --namespace {{ .Release.Namespace }} svc -w {{ include "openresty-art.fullname" . }}'
  export SERVICE_IP=$(kubectl get svc --namespace {{ .Release.Namespace }} {{ include "openresty-art.fullname" . }} --template "{{"{{ range (index .status.loadBalancer.ingress 0) }}{{.}}{{ end }}"}}")
  echo http://$SERVICE_IP:{{ .Values.service.port }}
# в случае   ClusterIP
{{- else if contains "ClusterIP" .Values.service.type }}
  export POD_NAME=$(kubectl get pods --namespace {{ .Release.Namespace }} -l "app.kubernetes.io/name={{ include "openresty-art.name" . }},app.kubernetes.io/instance={{ .Release.Name }}" -o jsonpath="{.items[0].metadata.name}")
  export CONTAINER_PORT=$(kubectl get pod --namespace {{ .Release.Namespace }} $POD_NAME -o jsonpath="{.spec.containers[0].ports[0].containerPort}")
  echo "Visit http://127.0.0.1:8080 to use your application"
  kubectl --namespace {{ .Release.Namespace }} port-forward $POD_NAME 8080:$CONTAINER_PORT
{{- end }}

```
##### ConfigMap
```
Целевая тема это монтирование конфигов через volumes
для тестовой версии можно через configmap
В директории templates:

  configmap-conf.yaml - содержит конфигурационный файл default.conf.
  configmap-html.yaml - содержит html файлы.
```
###### VARIANT 1
```
Файлы, которые находятся непосредственно в ConfigMaps, неудобно редактировать. Редакторы теряются в формате. Например, в configmap-html.yaml основной формат - yaml, а формат вложенных файлов html.
Идея вынести содержимое вложенных файлов в отдельный файл. А в шаблоне, в нужном месте вставлять его содержимое.

configmap-conf.yaml
Конфигурационный файла приложения. 
-  default.conf  (./K8S/helm/teach_example_chart/openresty-art/default.conf)
                  и поместим в него конфигурационные параметры openresty.
                  (./K8S/helm/teach_example_chart/base-application/configmap-conf.yaml)

Созаем директорию html (./K8S/helm/teach_example_chart/openresty-art/html)
                        где будут находиться дополнительные файлы 
index.html - берем из  (./K8S/helm/teach_example_chart/base-application/configmap-html.yaml)
50x.html   - берем из  (./K8S/helm/teach_example_chart/base-application/configmap-html.yaml)

configmap-conf-var1.yaml  (./K8S/helm/teach_example_chart/openresty-art/templates/configmap-conf-var1.yaml)
configmap-html-var1.yaml  (./K8S/helm/teach_example_chart/openresty-art/templates/configmap-html-var1.yaml)

В файле configmap-conf.yaml удалим содержимое секции data и вставим следующий шаблон.
```
```yaml
data:
  default.conf: |-
{{ .Files.Get "default.conf" | indent 4 }}
```
В шаблоне мы использовали встроенный объект Files. При помощи которого мы можем работать с файлами, находящимися внутри чарта.

При помощи функции Get получаем содержимое файла default.conf. Сдвигаем каждую строку на 4 символа. 
Шаблон должен быть помещен строго в начало строки.

Проверим, работает шаблон или нет.

helm template app ./openresty-art/ -f my-values.yaml > app.yaml
configmap-html.yaml

В фале configmap-html.yaml удалим все в разделе data и добавим следующий шаблон:
```yaml
data:
{{- range $path, $_ :=  .Files.Glob  "html/*" }}
  {{ base $path }}: |
{{ $.Files.Get $path | indent 4 }}
{{- end }}
```
```
При помощи функции Glob мы получаем список файлов из указанной директории, подходящих под шаблон. 
Glob - возвращает 2 значения путь $path и ошибку $_
При помощи range перебираем его. В каждой итерации в переменной %path получаем путь к файлу.
Функция base возвращает имя файла из полного пути 
$.Files.Get читает его содержимое.
В итоге, в configMap мы получим столько файлов, сколько их есть в директории html.

Проверяем:

helm template app ./openresty-art/ -f my-values.yaml > app.yaml

При использовании .Files мы не сможем изменить содержимое файлов при помощи кастомных файлов values и параметров --set. 
```
###### VARIANT 2
```
Позволяет реально заменять данные при установки helm чарта 
для этого
- в ./K8S/helm/teach_example_chart/openresty-art
  выносим каталог html на дирректорию выше в ./K8S/helm/teach_example_chart/ 

Добавить содержимое файлов default.conf и из каталога html  в файл values.yaml.

```
```yaml
conf:
  defaultConf: |-
    server {
        listen       80;
        server_name  localhost;

        location / {
            root   /usr/local/openresty/nginx/html;
            index  index.html index.htm;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/local/openresty/nginx/html;
        }
    }
html:
  index: |-
    <html>
      <head>
        <title>Тестовая страница</title>
        <meta charset="UTF-8">
      </head>
      <body>
        <h1>Тестовая страница</h1>
      </body>
    </html>
  50x: |-
    <!DOCTYPE html>
    <html>
    <head>
    <meta content="text/html;charset=utf-8" http-equiv="Content-Type">
    <meta content="utf-8" http-equiv="encoding">
    <title>Error</title>
    <style>
        body {
            width: 35em;
            margin: 0 auto;
            font-family: Tahoma, Verdana, Arial, sans-serif;
        }
    </style>
    </head>
    <body>
    <h1>An error occurred.</h1>
    <p>Sorry, the page you are looking for is currently unavailable.<br/>
    Please try again later.</p>
    </body>
    </html>
```    
В файле configmap-conf-var2.yaml (./K8S/helm/teach_example_chart/openresty-art/templates/configmap-conf-var2.yaml)

нам необходимо подставить всего один файл с известным именем. Поэтому шаблон будет простой.

```yaml
data:
  default.conf: |-
{{ .Values.conf.defaultConf | indent 4 }}
```
В файле configmap-html-var2.yaml (./K8S/helm/teach_example_chart/openresty-art/templates/configmap-conf-var2.yaml),  количество html файлов заранее не известно. Поэтому шаблон будет чуть сложнее.
```yaml
data:
{{- range $file, $value :=  .Values.html }}
  {{ $file }}.html: |
{{ $value | indent 4 }}
{{- end }}
```
```
Проверяем работу шаблона по умолчанию:

helm template app ./openresty-art/ -f my-values.yaml > app.yaml

Теперь посмотрим, как подставить свои файлы, при вызове helm. 
1 способ - перенести это в файл my-values/yaml
2 способ 
Создадим в директории (./K8S/helm/teach_example_chart)
          директорию html и поместим в неё файла index.html

Сначала подставим только my-default.conf:

# --set-file conf.defaultConf=my-default.conf
# заменяем conf.defaultConf=<имя файла>

helm template app ./openresty-art/ -f my-values.yaml \
                  --set-file conf.defaultConf=my-default.conf  > app.yaml

helm template app ./openresty-art/ -f my-values.yaml \
                  --set-file conf.defaultConf=my-default.conf \
                  --set-file html.index=html/index.html > app.yaml

Добавим 3-й html файл:

helm template app ./openresty-art/ -f my-values.yaml \
                  --set-file conf.defaultConf=my-default.conf \
                  --set-file html.test=html/index.html > app.yaml
```
##### Удалить лишнее
```
B файле values.yaml удаляем все параметры, не используемые в чарте. (в нашем случае все что не нужно закоменчено)
Проверка 

helm template app ./openresty-art > app.yaml
```
##### Добавить нужное
```
B первую очередь должна быть сформирована документация к чарту. Что бы другие люди могли без проблем его использовать.

Chart.yaml
Начнём с простого, добавим дополнительную информацию в Chart.yaml.
```
```yaml
home: https://github.com/j1nn33/study/blob/master/K8S/helm/teach_example_chart/README.md
maintainers:
  - name: teach helm chart
    email: 
    url: https://
```
```
values.yaml
В файле values.yaml добавить комментарии, описывающие параметры.

README.md
README.md - это основной файл документации по чарту.

```
##### Создать файл чарта
```
Для создания чарта используем команду package:
cd ./K8S/helm/teach_example_chart
helm package openresty-art
Итого будет создан файл openresty-art-0.1.0.tgz
```
##### Опубликовать чарт
```
# Для публикации чарта подойдёт любой WEB серверер. https://github.com/ 
# Создадим свое хранилище 
# 
# В директории helm создадим директорию charts.
# Перенесём в неё файл openresty-art-0.1.0.tgz. 
# 
# Перейдём в эту директорию и создадим файл index.yaml
# Для заполнения файла index.yaml  

# для каталога 
helm repo index .

# для https://github.com/ 
# helm repo index . --url по которому доступен этот бинарник https://raw.githubusercontent.com/j1nn33/study/blob/master/K8S/helm/charts

helm repo index . --url https://raw.githubusercontent.com/j1nn33/study/blob/master/K8S/helm/charts

# Запушим в github эту директорию со всеми файлами.
# После этого можно пользоваться чартом, находящимся в https://raw.githubusercontent.com/j1nn33/study/blob/master/K8S/helm/charts

# Добавление нового чарта 
#  - добавить файл с архивов в ./K8S/helm/charts
#  - helm repo index . --url https://raw.githubusercontent.com/j1nn33/study/blob/master/K8S/helm/charts

# Подключим репозиторий.

helm repo add openresty-art https://raw.githubusercontent.com/j1nn33/study/blob/master/K8S/helm/charts
helm repo update
helm repo list
helm search repo | grep openresty
Если git приватный, т.е. для доступа к нему требуется логин и пароль. При добавлении репозитория потребуется ввести эти логин и пароль.
```
