pipeline {
    agent any


    environment {
        imgname = "python1"
        imgtag  = "${BUILD_NUMBER}"
        dockerhub = "vivekthanth1"
    }


    stages {

        stage('First') {
            steps {
                sh 'git clone -f https://github.com/vivekthanth123-code/Placement.git'
            }
        }

        stage('Second') {
            steps {
                sh 'docker build -t ${dockerhub}/${imgname}:${imgtag} .'
            }
        }

        stage('Third') {
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
        stage('Fourth') {
            steps {
                sh 'docker container rm -f  python1-container'
            }
        }

        stage('Fifth') {
            steps {
                sh 'docker run -d -p 5000:5000 --name python1-container ${dockerhub}/${imgname}:${imgtag}'
            }
        }
    }
}
