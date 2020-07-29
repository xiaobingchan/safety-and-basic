pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '*/master']], browser: [$class: 'GithubWeb', repoUrl: 'https://github.com/xiaobingchan/github_jenkins_test'], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '837b6817-d03c-4efd-b2d3-eac4b9c12494', url: 'https://github.com/xiaobingchan/github_jenkins_test.git']]])
            }
        }
        stage('Test') {
            steps {
        sh '''
        cd /var/lib/jenkins/workspace/dfawdwadwa
        /usr/local/maven/bin/mvn package
        pwd
        ls
        '''
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
