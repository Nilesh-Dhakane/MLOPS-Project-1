pipeline {

    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'plasma-climber-480605-i6'
        GCLOUD_PATH = '/usr/bin'   // Correct default path inside Jenkins/Docker
    }

    stages {

        stage('Cloning GitHub Repo') {
            steps {
                echo 'Cloning GitHub repo in Jenkins'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    extensions: [],
                    userRemoteConfigs: [[
                        credentialsId: 'github_token',
                        url: 'https://github.com/Nilesh-Dhakane/MLOPS-Project-1.git'
                    ]]
                )
            }
        }

        stage('Setup Python Virtual Environment') {
            steps {
                echo 'Setting up virtual environment and installing libraries'
                sh '''
                    python -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                '''
            }
        }

        stage('Build and Push Docker Image to GCR') {
            steps {

                // ✅ FIXED: Credential ID must NOT contain spaces
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {

                    script {
                        echo 'Building and pushing Docker image to GCR'

                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            # ✅ FIXED: correct command
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                            gcloud config set project ${GCP_PROJECT}

                            # ✅ FIXED: correct spelling
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                            docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to google cloud run') {
            steps {

                // ✅ FIXED: Credential ID must NOT contain spaces
                withCredentials([
                    file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')
                ]) {

                    script {
                        echo 'Deploy to google cloud run'

                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            # ✅ FIXED: correct command
                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                            gcloud config set project ${GCP_PROJECT}

                            # ✅ FIXED: correct spelling
                            gcloud run deploy ml-project \ 
                                --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                                --platform=managed \ 
                                --region=us-central1 \
                                --allow=unauthenticated
                        '''
                    }
                }
            }
        }
    }
}




/*pipeline{

    agent any
    environment{
        VENV_DIR = 'venv'
        GCP_PROJECT = 'plasma-climber-480605-i6'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk-bin'
    }

    stages{
        stage('cloning github repo in jenkins'){
            steps{
                echo 'cloning github repo in jenkins'
                checkout scmGit(branches: [[name: 'main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github_token', url: 'https://github.com/Nilesh-Dhakane/MLOPS-Project-1.git']])
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
        stage('Building and pushing docker image in GCR'){
            steps{
                withCredentials(file(credentialsId:"GCP key", variable : "GOOGLE_APPLICATION_CREDENTIALS")){
                    script{
                        echo 'Building and pushing docker image in GCR'
                        sh '''
                        export PATH=$PATH:${GCLOUD_PATH}
                        gcloud auth-activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}

                        gcloud config set project ${GCP_PROJECT}

                        gcloud auth configure-docker --quite

                        docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                        docker push gcr.io/${GCP_PROJECT}/ml-project:latest 

                        '''
                    }
                }
            }
        }
    }
}
*/