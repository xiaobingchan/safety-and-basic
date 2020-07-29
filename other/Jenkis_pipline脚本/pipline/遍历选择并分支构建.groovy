node {
   stage('Preparation') {
        def sampleText =rtttt.split(',')
        for(String i in sampleText) {
            echo i;
        }
   }
   stage('Build') {
       checkout([$class: 'GitSCM', branches: [[name: '*/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '837b6817-d03c-4efd-b2d3-eac4b9c12494', url: 'https://github.com/xiaobingchan/github_jenkins_test.git']]])
   }
   stage('Results') {
       echo env.myass
   }
}