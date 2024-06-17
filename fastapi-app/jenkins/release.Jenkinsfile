// jenkins/release.Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Clone repository') {
            steps {
                git 'https://github.com/yourusername/fastapi-app.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                // Add your test commands here, for example:
                // sh 'pytest'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('yourusername/fastapi-app')
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', 'dockerhub-credentials') {
                        docker.image('yourusername/fastapi-app').push('release')
                    }
                }
            }
        }
    }
}
