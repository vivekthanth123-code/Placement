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
                    sed -i 's|image: django-app:.*|image: ${dockerhub}/${imgname}:${imgtag}|g' django-deployment.yaml
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

                        git add django-deployment.yaml
                        git commit -m "Update image to ${imgtag}" || true
                        git push origin main
                        '''
                    }
                }
            }
        
    }
}
