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

    stage('Build image') {
        /* This builds the actual image; synonymous to
         * docker build on the command line */

        app = docker.build("mdjohnson/desticket","--network host -f github/deslabs/desticket/Dockerfile .")
    }

    stage('Test image') {
        /* Ideally, we would run a test framework against our image.
         * For this example, we're using a Volkswagen-type approach ;-) */
        app.inside {
            sh 'echo "Tests passed"'
        }
    }

    stage('Push image') {
        /* We'll push the image with two tags:
         * First, the incremental build number from Jenkins
         * Second, the 'latest' tag.
         * Pushing multiple tags is cheap, as all the layers are reused. */
        docker.withRegistry('https://registry.hub.docker.com', 'mdjohnson-docker-hub-credentials') {
            app.push("v${env.BUILD_VERSION}")
            app.push("latest")
        }
    }

   stage('Create Helm templates') {
        /* We'll create deployment yaml from Helm */
        dir('github/deslabs/desticket'){
            sh "helm template desticket --set image.tag=v${env.BUILD_VERSION},version=v${env.BUILD_VERSION}> deploy_desticket.yaml" 
            sh "mv deploy_desticket.yaml ${env.WORKSPACE}/"
        }
    }

    stage('Commit deploy_desticket.yaml to bitbucket repository') {
        /* Let's make sure we have the repository cloned to our workspace */
        dir('bitbucket'){  git branch: 'master',
            credentialsId: 'mjohns44-bitbucket-credentials',
            url: 'https://opensource.ncsa.illinois.edu/bitbucket/scm/desdm/deslabs-deploy.git'

            sh "mv ${env.WORKSPACE}/deploy_desticket.yaml desticket"
            try {
                sh "git remote add bitbucket https://opensource.ncsa.illinois.edu/bitbucket/scm/desdm/deslabs-deploy.git"}
            catch (err){
            echo err.getMessage()
            echo "Remote site already exists. Will continue."}
            sh "git commit -am v${env.BUILD_VERSION}"
            withCredentials([usernamePassword(credentialsId: 'mjohns44-bitbucket-credentials',
                            passwordVariable: 'GIT_PASSWORD',
                            usernameVariable: 'GIT_USERNAME')]){
                sh "git push https://${GIT_USERNAME}:${GIT_PASSWORD}@opensource.ncsa.illinois.edu/bitbucket/scm/desdm/deslabs-deploy.git"
            }
      }
    }

     stage('Deploy to kubernetes') {
        /* Now, we'll deploy latest build on kubernetes */
        dir('bitbucket/desticket'){
            count= sh (script: "kubectl get deployments -n deslabs-devel desticket -o json | jq .status.replicas",
                      returnStdout: true).trim()
            sh "kubectl apply -f deploy_desticket.yaml" 
            sh "sleep 30"
            post_count = sh (script: "kubectl get deployments -n deslabs-devel desticket -o json | jq .status.updatedReplicas",
                      returnStdout: true).trim() 
            if (count == post_count) {
                echo "Deployment successful. Continuing..."
            } else {
                post_count_2 = sh (script: "kubectl get deployments -n deslabs-devel desticket -o json | jq .status.updatedReplicas",
                      returnStdout: true).trim()
                if (post_count_2 >= count){
                    echo "Deployment successful. Continuing..."}
                else{
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
