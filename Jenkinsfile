pipeline {
    agent any
    
    environment{
        VENV_DIR = 'venv'
    }
    
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


        stage('setting up our virtual environmetn and insstalling dependencies') {
            steps {
                script {
                    echo 'setting up our virtual environmetn and insstalling dependencies......'
                    sh '''
                    python -m vnev ${VNEV_DIR}
                    . ${VNEV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    '''
                    
                }
            }
        }

    }
}
