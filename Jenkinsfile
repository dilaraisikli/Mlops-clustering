pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        PYTHON   = 'python3'
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

        stage('setting up virtual environment and installing dependencies') {
            steps {
                script {
                    echo 'setting up virtual environment and installing dependencies......'
                    sh """
                        ${PYTHON} -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    """
                }
            }
        }
    }
}
