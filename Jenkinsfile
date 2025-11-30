pipeline {

    agent {
        node {
            label 'fedora'
        }
    }
    environment {
        REGISTRY_URL      = "10.88.19.170:5000"
        IMAGE_NAME        = "ise_user_portal"
        IMAGE_TAG         = "${BUILD_NUMBER}"
        SOURCE_REPO       = "https://github.com/gurkiratm/ISE_User_Portal.git"
        SOURCE_BRANCH     = "main"
        MANIFESTS_REPO_PATH    = "github.com/gurkiratm/cicd-ISE-manifests.git"
        MANIFESTS_REPO    = "https://${MANIFESTS_REPO_PATH}"
        MANIFEST_BRANCH    = "main"
        DEPLOYMENT_FILE    = "manifests/deploy-ise.yaml"
        CREDS_ID          = "927f5127-5f7d-4669-9d47-89e70681402c"
    }

    stages {
        stage('Init Workspace') {
            steps {
                echo 'Cleaning up workspace...'
                deleteDir()
            }
        }
        stage('checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                // git credentialsId: "${CREDS_ID}", url: "${SOURCE_REPO}", branch: "${SOURCE_BRANCH}"
            }
        }
        stage('Build Docker image') {
            steps {
                echo 'Building Docker image...'
                sh '''
                hostname
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
        stage('checkout K8s manifest repo') {
            steps {
                echo 'Cloning K8s configuration repository...'
                // git credentialsId: "${CREDS_ID}", url: "${MANIFESTS_REPO}", branch: "${MANIFEST_BRANCH}"
                script{
                    withCredentials([usernamePassword(credentialsId: "${CREDS_ID}",
                        passwordVariable: 'GIT_PASSWORD',
                        usernameVariable: 'GIT_USERNAME'
                    )]) {
                        sh '''
                        #rm -rf manifests-repo
                        git clone -b ${MANIFEST_BRANCH} https://${GIT_USERNAME}:${GIT_PASSWORD}@${MANIFESTS_REPO_PATH} manifests-repo
                        ls -lR manifests-repo/
                        '''
                    }
                }
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
                        cd manifests-repo
                        cp templates/deploy-template-ise.yaml manifests/deploy-ise.yaml
                        sed -i "s|__REGISTRY-URL__/__IMAGE-NAME__:__IMAGE-TAG__|${REGISTRY_URL}/${IMAGE_NAME}:${IMAGE_TAG}|" manifests/deploy-ise.yaml
                        cat -n manifests/deploy-ise.yaml
                        #sed -i "s|image: ${REGISTRY_URL}/${IMAGE_NAME}:.*|image: ${REGISTRY_URL}/${IMAGE_NAME}:${BUILD_NUMBER}|" manifests/deploy-ise.yaml
                        
                        git config list
                        #git config user.email "gurkiratmall207@gmail.com"
                        #git config user.name "gurkiratm"
                        #git config list

                        git add manifests/deploy-ise.yaml
                        git commit -m "Jenkins build ${BUILD_NUMBER}: Updating ISE User Portal deployment to image tag ${IMAGE_TAG}"
                        git push https://${GIT_USERNAME}:${GIT_PASSWORD}@${MANIFESTS_REPO_PATH} ${MANIFEST_BRANCH}
                        '''
                    }
                }
            }
        }
    }
}