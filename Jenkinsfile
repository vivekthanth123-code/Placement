pipeline {
    agent any

    environment {
        imgname   = "python1"
        imgtag    = "${BUILD_NUMBER}"
        dockerhub = "vivekthanth1"
    }

    stages {

        stage('Checkout App Repo') {
            steps {
                sh """
                    pwd
                    ls -al
                    """
                git branch: 'main',
                    url: 'https://github.com/vivekthanth123-code/Placement.git'
            }
        }

        stage('Build Image') {
            steps {
                sh '''
                docker build -t ${dockerhub}/${imgname}:${imgtag} .
                '''
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub',
                        usernameVariable: 'username',
                        passwordVariable: 'password'
                    )
                ]) {
                    sh '''
                    docker login -u ${username} -p ${password}
                    docker push ${dockerhub}/${imgname}:${imgtag}
                    '''
                }
            }
        }

        // stage('Checkout Manifest Repo') {
        //     steps {
        //         dir('manifest') {
        //             git branch: 'main',
        //                 url: 'https://github.com/vivekthanth123-code/manifest.git'
        //         }
        //     }
        // }
        stage('Checkout Manifest Repo') {
            steps {
                git branch: 'main', url: 'https://github.com/vivekthanth123-code/manifest.git'
                }
        }
        stage('Update Deployment') {
            steps {  
                    sh """
                    pwd
                    ls -al
                    sed -i 's|image: vivekthanth1/python1:.*|image: ${dockerhub}/${imgname}:${imgtag}|g' django-deployment.yaml
                    cat django-deployment.yaml
                    """
            }
        }

        stage('Push Manifest Changes') {
            steps {
                
                    withCredentials([
                        gitUsernamePassword(
                            credentialsId: 'github',
                            gitToolName: 'Default'
                        )
                    ]) {
                        sh '''
                        git config user.name "Jenkins"
                        git config user.email "jenkins@example.com"

                        git add .
                        git status
                        git commit -m "Update image to ${imgtag}" || true
                        git push origin main
                        '''
                    }
                }
            }
        stage('K8s deploy') {
            steps {
                script {
                    withCredentials([
                        sshUserPrivateKey(
                            credentialsId: 'k8skey',
                            keyFileVariable: 'identity',
                            usernameVariable: 'userName'
                        )
                    ]) {

                        def remote = [:]
                        remote.name = 'k8snode'
                        remote.host = '98.93.61.82'
                        remote.user = userName
                        remote.identityFile = identity
                        remote.allowAnyHosts = true

                        sshCommand remote: remote, command: 'cd ~/manifest  && git pull origin main && kubectl apply -f django-deployment.yaml'
                    }
                }
            }
        }
        
    }
}
