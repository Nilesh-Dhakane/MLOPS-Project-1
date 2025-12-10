pipeline{

    agent any
    environment{
        VENV_DIR = 'venv'
    }

    stages{
        stage('cloning github repo in jenkins'){
            steps{
                echo 'cloning github repo in jenkins'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_token', url: 'https://github.com/Nilesh-Dhakane/MLOPS-Project-1.git']])
            }
        }
        stage('setting up virtual environment in jenkins and installing librabries'){
            steps{
                echo 'setting up virtual environment in jenkins and installing librabries'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }
    }
}