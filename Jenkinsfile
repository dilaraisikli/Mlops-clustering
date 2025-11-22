pipeline {
    agent any

    stages {
        stage('cloning github repo to jenkins') {
            steps {
                script {
                    echo 'cloning github repo to jenkins......'
                    checkout(
                        scmGit(
                            branches: [[name: '*/main']],
                            extensions: [],
                            userRemoteConfigs: [[
                                credentialsId: 'github_token',
                                url: 'https://github.com/dilaraisikli/Mlops-clustering'
                            ]]
                        )
                    )
                }
            }
        }
    }
}
