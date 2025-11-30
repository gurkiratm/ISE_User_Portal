pipeline {
    agent any
    environment {
        REGISTRY_URL      = "10.88.19.170:5000"
        IMAGE_NAME        = "ise_user_portal"
        IMAGE_TAG         = "${BUILD_NUMBER}"
        MANIFESTS_REPO_PATH    = "github.com/gurkiratm/cicd-ISE-manifests.git"
        MANIFESTS_REPO    = "https://${MANIFESTS_REPO_PATH}"
        MANIFEST_BRANCH    = "main"
        DEPLOYMENT_FILE    = "manifests/deploy-ise.yaml"
        CREDS_ID          = "927f5127-5f7d-4669-9d47-89e70681402c"
    }

    stages {
        stage('checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build Docker image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                docker build -t ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }
        stage('Push to local registry') {
            steps {
                echo 'Pushing Docker image to local registry...'
                sh '''
                docker push ${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }
        stage('checkout K8s git') {
            steps {
                echo 'Cloning K8s configuration repository...'
                git credentialsId: "${CREDS_ID}", url: "${MANIFESTS_REPO}", branch: "${MANIFEST_BRANCH}"
            }
        }
        stage('Update K8s deployment and push changes') {
            steps {
                echo 'Updating K8s deployment file...'
                script {
                    withCredentials([usernamePassword(credentialsId: "${CREDS_ID}",
                        passwordVariable: 'GIT_PASSWORD',
                        usernameVariable: 'GIT_USERNAME'
                    )]) {
                        sh '''
                        cp templates/deploy-template-ise.yaml manifests/deploy-ise.yaml
                        sed -i 's|__REGISTRY-URL__/__IMAGE-NAME__:__IMAGE-TAG__|${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}|' manifests/deploy-ise.yaml
                        cat -n manifests/deploy-ise.yaml
                        #sed -i "s|image: ${REGISTRY_URL}/${IMAGE_NAME}:.*|image: ${REGISTRY_URL}/${IMAGE_NAME}:${BUILD_NUMBER}|" manifests/deploy-ise.yaml
                        
                        git config list
                        git config user.email "gurkiratmall207@gmail.com"
                        git config user.name "gurkiratm"
                        git config list

                        git add manifests/deploy-ise.yaml
                        git commit -m "Update ISE User Portal deployment to image tag ${IMAGE_TAG}"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${MANIFESTS_REPO_PATH} ${MANIFEST_BRANCH}
                        '''
                    }
                }
            }
        }
    }
}