## pipline
### - agent
### - options
### - parameters
### - enviroment
### - stages
### - when
### - steps
### - post
### - librares
### - parallel
### - matrix
## Основные шаги
### pipline
```yaml

pipeline {
    libraries {lib{"<lib_name>@master"}}
    agent {
        label 'clearAgent && (H2 || H3)' 
    }
    options {disableConcurrentBuilds() }
    parameters {
        booleanParam(   name: "BUILD",
                        defaultValue: false,
                        description: 'Buid back')
    }
    enviroment {
        JAVA_HOME = tool (name: 'openjdk-21.0.0_linux',
                          type: 'jdk')
        PATH = "${env.JAVA_HOME}/bin:${env.PATH}"                  
    }
    stages {
        stage('Build backend') {
            when {
                expression {
                    params.BUILD == true
                }
            }
            steps {
                echo "Build backend"
            }
        }
    }
    post {
        failure {
            echo "Build backend failure"
        }
        success {
            echo "Build backend success" 
        }
        always {
            cleanWs()
        } 
    }
}

```
#### - agent
```yaml

    agent {
        label 'clearAgent && (H2 || H3)' 
    }
```
```
узел  - общий термин для любой системы которая можнет запускать задания jenkins
agent - работают на узлай и предоставляют спецефичные возомжности. (разные агнеты для разных сборок)
        может быть указан как в основном определении конвеера так и/или на одельных этапах 
```
#### - options
```yaml

    options {disableConcurrentBuilds() }
```
```
не обязательная директива для указания свойсвт и занчений предопределенных параметров, которые должны применяться по всему конвееру
```
#### - parameters
```yaml

    parameters {
        booleanParam(   name: "BUILD",
                        defaultValue: false,
                        description: 'Buid back')
    }
```
```
не обязательная директива для указания параметров коневеера
входные параметры могут поступать от пользователя или API 
```

#### - enviroment
```yaml

    enviroment {
        JAVA_HOME = tool (name: 'openjdk-21.0.0_linux',
                          type: 'jdk')
        PATH = "${env.JAVA_HOME}/bin:${env.PATH}"                  
    }

```
```
не обязательная директива для указания имени и значения переменной 
может быть указана как на уровене pipeline так и на уровне stage (по завершению stage доступна для данного stage, по выходу из stage 
переменная удаляется) 
их можно переобределять 
```

#### - stages
```yaml

    stages {
        stage('Build backend') {
```
```
логически завершенный этап
```

#### - when
```yaml

            when {
                expression {
                    params.BUILD == true
                }
            }
 
```
```
пример - что параметр BUILD выставлен в true

- условие
  тестирует один или несколько блоков exeption на истиность (true/false)
  true  - код выполняется
  false - код не выполняется

beforeOptions - проверка до примения Options
beforeInput   - проверка до input
beforeAgent   - проверка до переключения Agent 
```

#### - steps
```yaml

            steps {
                echo "Build backend"
            }
        }
    }
 
```
```
самый низкий уроверь функциональности - атомарные задачи 
Параметры:
    <name>:<значение > 
    () - значит нет обязательного параметра 

- все это выполнится одинаково (зависит от соглашения в команде)
sh 'ls -lah'
sh script: 'ls -lah'
sh (script: 'ls -lah')
sh ([script: 'ls -lah']) - закидывание в sh набор команд описанных в файле 
```

#### - post
```yaml

    post {
        failure {
            echo "Build backend failure"
        }
        success {
            echo "Build backend success" 
        }
        always {
            cleanWs()
        } 
    }
}

```
```
может быть как для pipeline так для stage
выполняется после pipeline
   always:    выполняется всегда
   changed:   статус текущей сборки отличается от статуса предыдущей 
   success:   текущая сборака прошла успешно
   failure:   не успешно 
   unstable:  состояние сборки не стабльно
```

#### - librares
```yaml

    libraries {lib{"<lib_name>@master"}}

```
```
позволяет импортировать общие бибилиотеки (набор кода для работы с конвеером)
```

#### - parallel
```yaml

    stages {
        stage('Build backend') {
            when {
                expression {
                    params.BUILD == true
                }
            }
            paralel{ 
                stage ("Chrome") {
                    steps {
                        echo "Chrome"
                    }                
                }
                stage ("firefox") {
                    steps {
                        echo "firefox"
                    }                
                }
                stage ("Yandex") {
                    steps {
                        echo "Yandex"
                    }                
                }
            }
    }

```
```
паралельный запуск однотипных этапов на каждом из этапов можно опраеделить своего агента 
```

#### - matrix
```yaml

    stages {
        stage('matrix') {
            axes {
                axis {
                    name 'OS'
                    values 'linux', 'windows', 'mac'
                }
                axis {
                    name 'BROWSER'
                    values 'firefox', 'chrome', 'safari'
                }
            }
            exludes {
                exlude {
                    axis {
                        name 'OS'
                        value 'linux'
                    }
                    axis {
                        name 'BROWSER'
                        values 'safari'
                    }
                }
            }
            stages {
                stage("Matrixx hello") {
                    steps {
                        echo "${OS} - ${BROWSER}"
                    }
                }
            }      
        }
    }
    
}

```
```
матричный запуск одинковых этапов с разными настройками 
исключение - сборка под OS linux safari
```

### Основные шаги
```

```

