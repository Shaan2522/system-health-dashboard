pipeline {
    agent any

    environment {
        IMAGE_NAME = 'system-health-dashboard'
        PYTHON = 'C:\\Users\\shant\\AppData\\Local\\Programs\\Python\\Python39\\python.exe'
        DOCKER = 'C:\\Users\\shant\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                bat '"%PYTHON%" -m venv venv'
                bat 'venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat 'venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                bat 'venv\\Scripts\\python.exe -m pytest tests/ -v'
            }
        }

        stage('Build') {
            steps {
                bat '"%DOCKER%" build -t %IMAGE_NAME%:latest .'
            }
        }

        stage('Tag') {
            steps {
                bat '"%DOCKER%" tag %IMAGE_NAME%:latest %IMAGE_NAME%:%BUILD_NUMBER%'
            }
        }

        stage('Health Check') {
            steps {
                bat '"%DOCKER%" run -d -p 5050:5000 -e APP_ENV=ci --name health-check-%BUILD_NUMBER% %IMAGE_NAME%:%BUILD_NUMBER%'
                bat 'ping -n 6 127.0.0.1 > nul'
                bat 'curl -f http://localhost:5050/health'
            }
            post {
                always {
                    bat '"%DOCKER%" stop health-check-%BUILD_NUMBER% || exit 0'
                    bat '"%DOCKER%" rm health-check-%BUILD_NUMBER% || exit 0'
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully: dependencies installed, tests passed, image built, tagged, and health-checked.'
        }
        failure {
            echo 'Pipeline failed. Check the stage logs above for details.'
        }
    }
}