pipeline {
    agent any

    environment {
        APP_NAME = "hotel-management-system"
        PORT = "5000"
        PATH = "C:\\jenkins_py\\Scripts;C:\\jenkins_py;C:\\Users\\RAHUL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
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

        stage('Environment Check') {
            steps {
                echo '====================================='
                echo ' Stage 2: Checking Python & Tools'
                echo '====================================='
                bat 'python.exe --version'
                bat 'pytest.exe --version'
            }
        }

        stage('Automated Tests') {
            steps {
                echo '====================================='
                echo ' Stage 3: Running Automated Pytest Suite'
                echo '====================================='
                bat 'pytest.exe -v'
            }
        }

        stage('Docker Deployment') {
            steps {
                echo '====================================='
                echo ' Stage 4: Docker Container Deployment'
                echo '====================================='
                script {
                    def dockerStatus = bat(script: 'docker.exe info >nul 2>&1', returnStatus: true)
                    if (dockerStatus == 0) {
                        echo '[INFO] Docker daemon is active! Building image and running Docker Compose...'
                        bat 'docker.exe build -t hotel-management-system:latest .'
                        bat 'docker-compose.exe down || rem'
                        bat 'docker-compose.exe up --build -d'
                        echo 'Waiting for containers to initialize...'
                        bat 'timeout /t 15 /nobreak'
                        bat 'docker.exe exec hotel_web_app python seed.py'
                        echo 'Deployment via Docker containers completed successfully!'
                    } else {
                        echo '[WARNING] Docker daemon is not running.'
                        echo 'Note: Start Docker Desktop anytime to automatically trigger Dockerized containers.'
                        echo 'Proceeding with database seed & validation...'
                        bat 'python.exe seed.py'
                    }
                }
            }
        }

        stage('Verification & Health Check') {
            steps {
                echo '====================================='
                echo ' Stage 5: Database & Records Verification'
                echo '====================================='
                bat 'python.exe check_db.py'
            }
        }
    }

    post {
        success {
            echo '====================================================='
            echo ' [SUCCESS] Jenkins CI/CD Pipeline Completed Successfully!'
            echo ' Project: Hotel Management System'
            echo ' All Automated Tests: PASSED'
            echo ' Database & Seeder: VALIDATED'
            echo ' Admin Login: admin@hotel.com / Admin@123'
            echo ' Receptionist: receptionist@hotel.com / Receip@123'
            echo ' Manager: manager@hotel.com / Manager@123'
            echo '====================================================='
        }
        failure {
            echo '====================================================='
            echo ' [FAILURE] Pipeline failed. Check console output.'
            echo '====================================================='
        }
    }
}
