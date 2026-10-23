pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\omarm\\AppData\\Local\\Programs\\Python\\Python314\\python.exe'

        JWT_SECRET = credentials('jwt-secret')
        OMAR_PASSWORD = credentials('omar-password')
        YAMAL_PASSWORD = credentials('yamal-password')
        ADMIN_PASSWORD = credentials('admin-password')
    }

    stages {
        stage('Setup') {
            steps {
                bat 'if exist .venv rmdir /s /q .venv'
                bat '"%PYTHON%" -m venv .venv'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
                bat '.venv\\Scripts\\python.exe -m pip install -e helper_package'
            }
        }

        stage('Static analysis') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat '.venv\\Scripts\\python.exe -m bandit -r application_api resource_service processing_service > reports\\bandit.txt'
            }
        }

        stage('Dependency analysis') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pip_audit -r requirements.txt > reports\\pip-audit.txt 2>&1'
            }
        }

        stage('Start services') {
            steps {
                bat 'start "" /B .venv\\Scripts\\python.exe resource_service\\app.py > reports\\resource_service.log 2>&1'
                bat 'start "" /B .venv\\Scripts\\python.exe processing_service\\app.py > reports\\processing_service.log 2>&1'
                bat 'start "" /B .venv\\Scripts\\python.exe application_api\\app.py > reports\\application_api.log 2>&1'
                powershell 'Start-Sleep -Seconds 3'
            }
        }

        stage('Tests') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pytest tests -v --junitxml=reports\\pytest.xml > reports\\pytest.txt'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
            junit allowEmptyResults: true, testResults: 'reports/pytest.xml'
        }
    }
}