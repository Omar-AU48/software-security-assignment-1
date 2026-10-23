pipeline {
    agent any

    environment {
        JWT_SECRET = credentials('jwt-secret')
        OMAR_PASSWORD = credentials('omar-password')
        YAMAL_PASSWORD = credentials('yamal-password')
        ADMIN_PASSWORD = credentials('admin-password')
    }

    stages {
        stage('Install dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pip install -e helper_package'
            }
        }

        stage('Static analysis') {
            steps {
                bat 'if not exist reports mkdir reports'
                bat 'bandit -r application_api resource_service processing_service > reports\\bandit.txt'
            }
        }

        stage('Dependency analysis') {
            steps {
                bat 'pip-audit -r requirements.txt > reports\\pip-audit.txt'
            }
        }

        stage('Start services') {
            steps {
                bat 'start "" /B python resource_service\\app.py > reports\\resource_service.log 2>&1'
                bat 'start "" /B python processing_service\\app.py > reports\\processing_service.log 2>&1'
                bat 'start "" /B python application_api\\app.py > reports\\application_api.log 2>&1'
                bat 'timeout /t 3 /nobreak'
            }
        }

        stage('Tests') {
            steps {
                bat 'python -m pytest tests -v --junitxml=reports\\pytest.xml > reports\\pytest.txt'
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