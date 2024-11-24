#### Структура Helm Chart
```
https://helm.sh/docs/topics/charts/  


--chart_name                     
  |_ Chart.yaml                      # основной файл содержащий информацию о Helm Chart
  |_ values.yaml           
  |_ values.schema.json              # схема для валидации values.yaml
  |_ README.md
  |_ LICENSE
  |_ .helm
  |_ charts/                         # зависимые helm charts
  |_ crds/ 
  |_ tests
  |  |_test.yaml  
  |_templates/                       # содержит шаблоны манифестов      
     |_ deployment.yaml
     |_ hpa.yaml
     |_ ingress.yaml
     |_ NOTES.txt                    # сообщения в конце установки helm
     |_ service.yaml
     |_serviceaccount.yaml
     |_ *.tpl
```
###### Chart.yaml 
```yaml
apiVersion: v2        # The chart API version (required)
name: Name            # The name of the chart (required)
version: 0.1.1        # A SemVer 2 version (required)
kubeVersion:          # A SemVer range of compatible Kubernetes versions (optional)
description:          # A single-sentence description of this project (optional)
type: application     # The type of the chart (optional)
keywords:             # A list of keywords about this project (optional)
  - app1
  - istio
  - demo_chart                   
home:                 # The URL of this projects home page (optional)
sources:
  - https://___       # A list of URLs to source code for this project (optional)
dependencies:         # A list of the chart requirements (optional)
  - name: istio       # The name of the chart (nginx)
    version: 1.16.0   # The version of the chart ("1.2.3")
    repository:       # (optional) The repository URL ("https://example.com/charts") or alias ("@repo-name")
    condition:        # (optional) A yaml path that resolves to a boolean, used for enabling/disabling charts (e.g. subchart1.enabled )
    tags:             # (optional)
      - tag1          # Tags can be used to group charts for enabling/disabling together
      - tag2
    import-values:    # (optional)
      - values1
      - values3      # ImportValues holds the mapping of source values to parent key to be imported. Each item can be a string or pair of child/parent sublist items.
    alias:           # (optional) Alias to be used for the chart. Useful when you have to add the same chart multiple times
maintainers:         # (optional)
  - name:            # The maintainers name (required for each maintainer)
    email:           # The maintainers email (optional for each maintainer)
    url:             # A URL for the maintainer (optional for each maintainer)
icon:                # A URL to an SVG or PNG image to be used as an icon (optional).
appVersion:          # The version of the app that this contains (optional). Needn't be SemVer. Quotes recommended.
deprecated:          # Whether this chart is deprecated (optional, boolean)
annotations:
  example:           # A list of annotations keyed by name (optional).
```
###### tests
```
Содержит тесты в виде манифеста Pod с описанием контейнера с заданой командой 
для запуска теста. 
Контейнер должне успешно завершиться (RC == 0)
Созданый контейнер должнен содержать аннотацию 
helm.sh/hook: test
```
######  *.tpl
```
Содержит шаблоны и функции, которые доступны всему чарту.
Результаты шаблонизации этих файлов не попадают в итоговый набор манифестов
```