pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yourdockeruser/sample-python-microservice'
        DOCKER_CREDENTIALS_ID = 'docker-repo-credentials' // Docker credentials stored in Jenkins
        DATABASE_URL = 'postgresql://postgres:password@localhost:5432/users_db'
        DB_CONTAINER_NAME = 'jenkins_db'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the repository
                git branch: 'main', url: 'https://github.com/yourrepo/sample-python-microservice.git'
            }
        }

        stage('Setup Database') {
            steps {
                // Start a PostgreSQL database in a Docker container for testing
                sh '''
                docker run -d --name ${DB_CONTAINER_NAME} -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=users_db -p 5432:5432 postgres:13
                '''
                // Wait for the database to be ready
                sleep 20
            }
        }

        stage('Install Dependencies') {
            steps {
                // Install Python dependencies
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                // Run unit tests with DATABASE_URL
                withEnv(['DATABASE_URL=postgresql://postgres:password@localhost:5432/users_db']) {
                    sh 'pytest tests/'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                // Build the Docker image for the microservice
                sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} ."
            }
        }

        stage('Push Docker Image') {
            steps {
                // Push the Docker image to the repository
                withCredentials([usernamePassword(credentialsId: "${DOCKER_CREDENTIALS_ID}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker push ${DOCKER_IMAGE}:${BUILD_NUMBER}
                    '''
                }
            }
        }

        stage('Cleanup') {
            steps {
                // Remove PostgreSQL container
                sh "docker stop ${DB_CONTAINER_NAME} && docker rm ${DB_CONTAINER_NAME}"
            }
        }
    }

    post {
        always {
            // Cleanup Docker resources if necessary
            sh 'docker system prune -f'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}
