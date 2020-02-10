node {
    def app
    def count
    def post_count
    env.BUILD_VERSION = divide_build_number()

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        dir("github"){
            checkout scm
        }
    }

     stage('Deploy to kubernetes') {
        /* Now, we'll deploy latest build on kubernetes */
        dir('deployment_public/'){
            count= sh (script: "kubectl get deployments -n <> desticket -o json | jq .status.replicas",
                      returnStdout: true).trim()
            sh "./scripts/deploy -c -n -u" 
            sh "sleep 90"
            post_count = sh (script: "kubectl get deployments -n  desticket -o json | jq .status.updatedReplicas",
                      returnStdout: true).trim() 
            if (post_count >= count) {
                echo "Deployment successful. Continuing..."
            } else {
                sh "sleep 90"
                post_count_2 = sh (script: "kubectl get deployments -n <> desticket -o json | jq .status.updatedReplicas",
                      returnStdout: true).trim()
                if (post_count_2 >= count) {
                    echo "Deployment successful. Continuing..."
                } else {
                    error("Deployment failed. Exiting...")}
            }
            }
     }

    stage('Clean up unused docker builds') {
        sh "docker system prune -a -f"
    }
   
}

def divide_build_number(){
    node {
        build_version = env.BUILD_NUMBER.toLong() / 100.0
        build_version_float = build_version.toFloat()
        return String.format("%.2f",build_version_float)
    }
}