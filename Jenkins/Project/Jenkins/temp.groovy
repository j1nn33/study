pipeline {
    agent {
        node ('linux')
    }
    options{
        timestamps()
        ansiColos('xterm')
        buildDiscarder(
            logRotator(
                daysToKeepStr: '3',
                numToKeepStr: '3',
                artifactDaysToKeepStr: '3',
                artifactnumToKeepStr: '3',
            )
        )
        disableConcurrentDuilds()
        skipDefaultCheckout()
    }
    parameters{
        string    (name: 'ANSIBLE_USER',    description:'ansible user, become user', defaultValue: '')   
        password  (name: 'ANSIBLE_PASSWORD', description:'ansible user password',     defaultValue: '')
        string    (name: 'NODE_ADDRESS',    description:'Адреса нод, через запятую', defaultValue: '127.0.0.1')
    }
    stages {
        stage ('INIT') {
            steps {
                cleanWs()
                script{
                    checkout scm
                    sh 'ls -la'
                }
            }
        }
        stage('fix file krb5.conf') {
            steps{
                wrap([$class: "MaskPasswordsBuildWrapper", varPasswordPairs: [[password: "${params.ANSIBLE_PASSWORD}", var: 'PASSWORD']]]){
                    ansiblePlaybook(
                    extras: " -e ansible_ssh_user=${params.ANSIBLE_USER} -e ansible_ssh_password=${params.ANSIBLE_PASSWORD}",  
                    playbook: "./Project/Ansible/fix_client/playbook/after_client.yaml"
                    disableHostKeyChecking: true,
                    inventory: "${params.NODE_ADDRESS}"
                    forks: 5,
                    installation: 'ansible29'
                    colorized: true,
                    sudoUser: null
                    )
                }
            }
        }
    }
}