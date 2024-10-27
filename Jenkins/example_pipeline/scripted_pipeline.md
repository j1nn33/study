## scripted pipeline
### - пример 
### - импорт необходимых пакетов и расширений Groovy
### - аннотация @Library для подключения внешней библиотеки 
### - определение перемнных
### - определение свойств для текущего pipeline
### - определение узла, на котором будет производиться сборка
### - try - блок в котором происходит основеная часть сборки 
#### - проверка параметров  
#### - else
#### - cathc обработка исключений 
#### - finally
### - параллельный запуск





## scripted pipeline
### - пример
```yaml
import groovy.transform.Field
import org.jenkinsci.plugins.workflow.libs.Library
import org.jenkinsci.plugins.pipeline.modeldefinition.Utils

@Library(['libraryDevelop@v1.4']) _

def projectName = 'My project'

@Field Map services = [
    ui  : [source: [url: "ssh://git......", branch: "ui"]],
    back: [source: [url: "ssh://git......", branch: "back"]]
]
List<string> selectedService = ['ui', 'back', 'border']

properties([disableConcurrentBuilds(),
            parameters {[booleanParam(name: "BUILD", defaultValue: true, description: 'Buid back')]),
            pipelineTriggers([cron('0 */2 * * *')])
])

node('clearAgent && (H2 || H3)') {
    try {
        echo "Начало сборки" + projectName
        stage ('Build') {
            if (params.Build) {
                service.each { name, values ->
                    if (selectedService.collect { it.trim() }.contains(name)) {
                        sh("mkdir -p $(name) || true")
                        dir(name) {
                            echo ("Получен исходный код для " + name + " из ветки " + values.source.branch)
                            echo ("Заупустили сборку для " + name )
                        }
                    }
                } 
            } 
            else {
                Utils.markStageSkippedForConditional ('Build')
            }
        }
        echo "Начало сборки" + projectName
    } catch (Exception e) {
        echo ("Error: " + e.toString())
    } finally {
        echo ("Статус сборки: $currentResult")
    }
}

```

### - импорт необходимых пакетов и расширений Groovy

```
import groovy.transform.Field
import org.jenkinsci.plugins.workflow.libs.Library
import org.jenkinsci.plugins.pipeline.modeldefinition.Utils
```
### - аннотация @Library для подключения внешней библиотеки 

```
@Library(['libraryDevelop@v1.4']) _  должны загрузить библиотеку и присвоить ей _ 
_ означет что можно обращаться без явного указания имени 
```
### - определение перемнных

```
переменные:
   projectName     - название проекта  
   service         - словарь где ключи имена сервисов, значения инфо о репозитории, ветка
   selectedService - коллекция сервисов, которые подают в список собираемых сервисов 

def projectName = 'My project'                                 

@Field Map services = [
    ui  : [source: [url: "ssh://git......", branch: "ui"]],
    back: [source: [url: "ssh://git......", branch: "back"]]
]
List<string> selectedService = ['ui', 'back', 'border']

properties([disableConcurrentBuilds(),
            parameters {[booleanParam(name: "BUILD", defaultValue: true, description: 'Buid back')]),
            pipelineTriggers([cron('0 */2 * * *')])   # запускает собрку каждые 2 часа 
])
```

### - определение свойств для текущего pipeline
```
properties([disableConcurrentBuilds(),
            parameters {[booleanParam(name: "BUILD", defaultValue: false, description: 'Buid back')]),
            pipelineTriggers([cron('0 */2 * * *')])
])
```

### - определение узла, на котором будет производиться сборка
```
node('clearAgent && (H2 || H3)') {
```

### - try - блок в котором происходит основеная часть сборки 
```
    try {
        echo "Начало сборки" + projectName
  
    }
```

#### - проверка параметров  
```
- проверяется значение Build если оно false, то стадия помечается как пропущенная  
- service.each { name, values ->
  для каждого сервиса в словаре service проверяется, содержится ли он в списке selectedService
  если да, то выполняются следующие действия
      - создается дирректория с имененм сервиса 
      - внутри директории выполняется команда для клонирования репозитория
      - выполняется команда для сборки проекта

if (params.Build) {
    service.each { name, values ->
        if (selectedService.collect { it.trim() }.contains(name)) {
            sh("mkdir -p $(name) || true")
                dir(name) {
                    echo ("Получен исходный код для " + name + " из ветки " + values.source.branch)
                    echo ("Заупустили сборку для " + name )
```

#### - else
```
стадия помечается как пропущенная
    else {
        Utils.markStageSkippedForConditional ('Build')
```

#### - cathc обработка исключений 

```
    } catch (Exception e) {
        echo ("Error: " + e.toString())
```

#### - finally
```
    } finally {
        echo ("Статус сборки: $currentResult")
    }
```

### - параллельный запуск
```
используется словарь замыканий 
    все что внутри {} - замыкания и можем использовать в перемнной Closure

переменной myBuilds[name] =  присаиваем кусок кода 


Map<String,Closure> myBuilds = [:]
.....
    stage ('Build') {
        if (params.Build) {
            service.each { name, values ->
                if (selectedService.collect { it.trim() }.contains(name)) {
                    myBuilds[name] = {
                       sh("mkdir -p $(name) || true")
                            dir(name) {
                                echo ("Получен исходный код для " + name + " из ветки " + values.source.branch)
                                echo ("Заупустили сборку для " + name ) 
                    }
                }
            }
            if (myBuilds.size()!=0){
                paralle(myBuilds)
            }     
        } else  tils.markStageSkippedForConditional ('Build')          
    }


```