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

#  описание pipeline jenkins для запуска роли prometheus_role.yaml(пароли sudo зашиты в jenkins)
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
                ansiblePlaybook colorized: true, disableHostKeyChecking: true, credentialsId: 'ssh_cred_for_host', installation: 'ansible-master', inventory: './ROLES/ansible/inventory_monitoring/dev/hosts.ini', playbook: './ROLES/ansible/playbooks_monitoring/prometheus_role.yaml'   
                
            }    
        }
    }    
}
