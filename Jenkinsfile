import com.package.Commands;
@Library('devops-repo@master') _

pipeline{
    agent any

    tools {
      nodejs '12.9.1'
    }

    options {
        buildDiscarder logRotator(numToKeepStr: '5')
        disableConcurrentBuilds()
        timestamps()
    }

    environment {
            ENV = getEnvName(GIT_BRANCH)
            MAIL_TO = "email@address.com"
    }

    stages{
        stage('Build'){
            steps {
                sh """
                    python3 -m venv env
                    source env/bin/activate
                    cd email-sender-lambda
                    mkdir -p deps/python
                    docker run --name $ENV-email-sender-alinux amazonlinux:latest /bin/sh -c "yum install -y python3-pip;pip3 install boto3 -t /deps/python;rm -r /deps/python/*.dist-info ;rm -r /deps/python/__pycache__;"
                    docker cp $ENV-email-sender-alinux:/deps/python deps
                    pip install -r requirements.txt -t .
                    mv deps ../deps
                    zip -r lambda_code.zip . *
                    ls -a
                    mv ../deps deps
                    serverless deploy --stage $ENV
                    deactivate env
                """
            }
        }
    }

    post {
        always {
             sh """
                  docker rm $ENV-email-sender-alinux
                """
            cleanWs()
        }

        failure {
            emailext (
                    subject: "Job $JOB_NAME $BUILD_NUMBER is failed",
                    body: "Please take a look of the build logs $BUILD_URL",
                    to: "$MAIL_TO"
            )
        }

        unstable {
            emailext (
                    subject: "Job $JOB_NAME $BUILD_NUMBER is failed",
                    body: "Please take a look of the build logs $BUILD_URL",
                    to: "$MAIL_TO"
            )
        }

    }

}

private static String getEnvName(GIT_BRANCH){
    if ("origin/dev" == GIT_BRANCH) {
        return "dev"
    } else if ("origin/stg" == GIT_BRANCH) {
        return "stg"
    } else if ("origin/master" == GIT_BRANCH) {
        return "production"
    } else if ("origin/sandbox" == GIT_BRANCH) {
        return "sandbox"
    }
    else {
        return "dev"
    }
}

private static String getAccountId(GIT_BRANCH){
    if ("origin/master" == GIT_BRANCH) {
        return "1234567890"
    } else {
        return "0987654321"
    }
}
