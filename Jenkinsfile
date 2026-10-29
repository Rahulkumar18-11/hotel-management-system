pipeline {
    agent any

    environment {
        APP_NAME = "hotel-management-system"
        PORT = "5000"
        PATH = "C:\\Users\\RAHUL\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\RAHUL\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python313\\Scripts;C:\\Users\\RAHUL\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin;${env.PATH}"
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
                bat 'python --version'
                bat 'pip --version'
            }
        }

        stage('Automated Tests') {
            steps {
                echo '====================================='
                echo ' Stage 3: Running Automated Pytest Suite'
                echo '====================================='
                bat 'python -m pytest -v'
            }
        }

        stage('Docker Deployment') {
            steps {
                echo '====================================='
                echo ' Stage 4: Docker Container Deployment'
                echo '====================================='
                script {
                    def dockerStatus = bat(script: 'docker info >nul 2>&1', returnStatus: true)
                    if (dockerStatus == 0) {
                        echo '[INFO] Docker daemon is running! Proceeding with Docker build & deployment...'
                        bat 'docker build -t hotel-management-system:latest .'
                        bat 'docker-compose down || rem'
                        bat 'docker-compose up --build -d'
                        echo 'Waiting for containers to initialize...'
                        bat 'timeout /t 15 /nobreak'
                        bat 'docker exec hotel_web_app python seed.py'
                        echo 'Deployment via Docker completed!'
                    } else {
                        echo '[WARNING] Docker daemon is not currently running.'
                        echo 'To deploy via Docker: start Docker Desktop and rerun the build.'
                        echo 'Validating database schema and seeding local database...'
                        bat 'python seed.py'
                    }
                }
            }
        }

        stage('Verification & Health Check') {
            steps {
                echo '====================================='
                echo ' Stage 5: Database & Records Verification'
                echo '====================================='
                bat 'python check_db.py'
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
