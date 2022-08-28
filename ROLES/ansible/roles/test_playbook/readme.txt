#  описание pipeline jenkins для запуска тестового (пароли не требуются)

pipeline {
    agent {
        label 'master'
    }
    stages {
        stage('git') { // download from git
            steps {
                git branch: 'master', url: "https://github.com/j1nn33/study.git" // используем встроенный в Jenkins плагин Git для скачивания проекта из бранча main
            }
        }
        
        stage('execute Ansible') {
            steps {
                ansiblePlaybook colorized: true, disableHostKeyChecking: true, installation: 'ansible-master', inventory: './ROLES/ansible/roles/test_playbook/inventory.ini', playbook: './ROLES/ansible/roles/test_playbook/test_playbook.yaml'   
            }    
        }
    }    
}