pipeline {
    agent any

    environment {
        APP_NAME = "hotel-management-system"
        PORT = "5000"
        PATH = "C:\\Users\\RAHUL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
    }

    stages {
        stage('Checkout') {
            steps {
                echo '====================================='
                echo ' Stage 1: Checkout Source Code'
                echo '====================================='
                checkout scm
            }
        }

        stage('Docker Version Check') {
            steps {
                echo '====================================='
                echo ' Stage 2: Verifying Docker Availability'
                echo '====================================='
                bat 'docker version'
            }
        }

        stage('Docker Build') {
            steps {
                echo '====================================='
                echo ' Stage 3: Building Application Docker Image'
                echo '====================================='
                bat 'docker build -t hotel-management-system:latest .'
            }
        }

        stage('Deploy Containers') {
            steps {
                echo '====================================='
                echo ' Stage 4: Starting App & MongoDB Containers'
                echo '====================================='
                bat 'docker-compose down || rem'
                bat 'docker-compose up --build -d'
            }
        }

        stage('Wait for Services') {
            steps {
                echo '====================================='
                echo ' Stage 5: Waiting for Services & DB Health'
                echo '====================================='
                bat 'timeout /t 15 /nobreak'
            }
        }

        stage('Seed Database') {
            steps {
                echo '====================================='
                echo ' Stage 6: Seeding Initial Demo Data & Admin'
                echo '====================================='
                bat 'docker exec hotel_web_app python seed.py'
            }
        }

        stage('Verify Health Check') {
            steps {
                echo '====================================='
                echo ' Stage 7: Verifying Deployment Health'
                echo '====================================='
                bat 'curl.exe -s -o NUL -w "%%{http_code}" http://localhost:5000/'
                echo 'Application is live at http://localhost:5000'
            }
        }
    }

    post {
        success {
            echo '====================================================='
            echo ' [SUCCESS] Hotel Management System Successfully Deployed!'
            echo ' URL: http://localhost:5000'
            echo ' Admin Credentials: admin@hotel.com / Admin@123'
            echo '====================================================='
        }
        failure {
            echo '====================================================='
            echo ' [FAILURE] Pipeline failed. Check console output.'
            echo '====================================================='
        }
    }
}
