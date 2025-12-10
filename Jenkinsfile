pipeline{
    agent any
    stages{
        stage('cloning github repo in jenkins'){
            steps{
                echo 'cloning github repo in jenkins'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_token', url: 'https://github.com/Nilesh-Dhakane/MLOPS-Project-1.git']])
            }
        }
    }
}