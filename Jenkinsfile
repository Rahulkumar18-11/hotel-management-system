pipeline {
    agent any

    environment {
        APP_NAME = "hotel-management-system"
        PORT = "5000"
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

        stage('Docker Build') {
            steps {
                echo '====================================='
                echo ' Stage 2: Building Application Docker Image'
                echo '====================================='
                bat 'docker build -t hotel-management-system:latest .'
            }
        }

        stage('Deploy Containers') {
            steps {
                echo '====================================='
                echo ' Stage 3: Starting App & MongoDB Containers'
                echo '====================================='
                bat 'docker-compose down || rem'
                bat 'docker-compose up --build -d'
            }
        }

        stage('Wait for Services') {
            steps {
                echo '====================================='
                echo ' Stage 4: Waiting for Services & DB Health'
                echo '====================================='
                bat 'timeout /t 15 /nobreak'
            }
        }

        stage('Seed Database') {
            steps {
                echo '====================================='
                echo ' Stage 5: Seeding Initial Demo Data & Admin'
                echo '====================================='
                bat 'docker exec hotel_web_app python seed.py'
            }
        }

        stage('Verify Health Check') {
            steps {
                echo '====================================='
                echo ' Stage 6: Verifying Deployment Health'
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
