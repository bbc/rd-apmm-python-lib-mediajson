@Library("rd-apmm-groovy-ci-library@v1.x") _

/*
 Runs the following steps in parallel and reports results to GitHub:
 - Lint using flake8
 - Run Python 3 unit tests in tox
 - Build Debian packages for supported Ubuntu versions

 If these steps succeed and the main branch is being built, wheels and debs are uploaded to Artifactory and the
 R&D Debian mirrors.

 Optionally you can set FORCE_PYUPLOAD to force upload to Artifactory, and FORCE_DEBUPLOAD to force Debian package
 upload on non-main branches.
*/

pipeline {
    agent {
        label "ubuntu&&apmm-agent"
    }
    options {
        ansiColor('xterm') // Add support for coloured output
        buildDiscarder(logRotator(numToKeepStr: '10')) // Discard old builds
    }
    parameters {
        booleanParam(name: "FORCE_PYUPLOAD", defaultValue: false, description: "Force Python artifact upload")
        booleanParam(name: "FORCE_DEBUPLOAD", defaultValue: false, description: "Force Debian package upload")
    }
    triggers {
        cron(env.BRANCH_NAME == 'main' ? 'H H(0-8) * * *' : '') // Build main some time every morning
    }
    environment {
        http_proxy = "http://www-cache.rd.bbc.co.uk:8080"
        https_proxy = "http://www-cache.rd.bbc.co.uk:8080"
        PATH = "$HOME/.pyenv/bin:$PATH"
    }
    stages {
        stage("Clean Environment") {
            steps {
                sh 'git clean -dfx'
                sh 'rm -rf /tmp/$(basename ${WORKSPACE})/'
            }
        }
        stage("Prepare for build") {
            steps {
                bbcStagePyenvEnsureVersion("3.10")
            }
        }
        stage ("Linting Check") {
            steps {
                script {
                    env.lint_result = "FAILURE"
                }
                bbcGithubNotify(context: "lint/flake8", status: "PENDING")
                withBBCRDPythonArtifactory {
                   sh 'make lint'
                }
                script {
                    env.lint_result = "SUCCESS" // This will only run if the sh above succeeded
                }
            }
            post {
                always {
                    bbcGithubNotify(context: "lint/flake8", status: env.lint_result)
                }
            }
        }
        stage ("Type Check") {
            steps {
                script {
                    env.mypy_result = "FAILURE"
                }
                bbcGithubNotify(context: "type/mypy", status: "PENDING")
                withBBCRDPythonArtifactory {
                   sh 'make mypy'
                }
                script {
                    env.mypy_result = "SUCCESS" // This will only run if the sh above succeeded
                }
            }
            post {
                always {
                    bbcGithubNotify(context: "type/mypy", status: env.mypy_result)
                }
            }
        }
        stage ("Python Unit Tests") {
            steps {
                script {
                    env.unittest_result = "FAILURE"
                }
                bbcGithubNotify(context: "tests/unit", status: "PENDING")
                withBBCRDPythonArtifactory {
                   sh 'make test'
                }
                script {
                    env.unittest_result = "SUCCESS" // This will only run if the sh above succeeded
                }
            }
            post {
                always {
                    bbcGithubNotify(context: "tests/unit", status: env.unittest_result)
                }
            }
        }
        stage ("Debian Source Build") {
            steps {
                script {
                    env.debSourceBuild_result = "FAILURE"
                }
                bbcGithubNotify(context: "deb/sourceBuild", status: "PENDING")

                withBBCRDPythonArtifactory {
                   sh 'rm -rf deb_dist'
                    sh 'python ./setup.py sdist'
                    sh 'make dsc'
                    bbcPrepareDsc()
                }
                stash(name: "deb_dist", includes: "deb_dist/*")
                script {
                    env.debSourceBuild_result = "SUCCESS" // This will only run if the steps above succeeded
                }
            }
            post {
                always {
                    bbcGithubNotify(context: "deb/sourceBuild", status: env.debSourceBuild_result)
                }
            }
        }
        stage ("Build with pbuilder") {
            steps {
                bbcGithubNotify(context: "deb/packageBuild", status: "PENDING")
                // Build for all supported platforms and extract results into workspace
                bbcParallelPbuild(stashname: "deb_dist",
                                    dists: bbcGetSupportedUbuntuVersions(),
                                    arch: "amd64")
            }
            post {
                success {
                    archiveArtifacts artifacts: "_result/**"
                }
                always {
                    // currentResult is governed by the outcome of the pbuilder steps at this point, so we can use it
                    bbcGithubNotify(context: "deb/packageBuild", status: currentBuild.currentResult)
                }
            }
        }
        stage ("Upload Packages") {
            // Duplicates the when clause of each upload so blue ocean can nicely display when stage skipped
            when {
                anyOf {
                    expression { return params.FORCE_PYUPLOAD }
                    expression { return params.FORCE_DEBUPLOAD }
                    expression {
                        bbcShouldUploadArtifacts(branches: ["main", "dev"])
                    }
                }
            }
            stages {
                stage ("Upload to PyPi") {
                    when {
                        anyOf {
                            expression { return params.FORCE_PYUPLOAD }
                            expression {
                                bbcShouldUploadArtifacts(branches: ["main"])
                            }
                        }
                    }
                    steps {
                        script {
                            env.pypiUpload_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "pypi/upload", status: "PENDING")
                        sh 'rm -rf dist/*'
                        bbcMakeGlobalWheel("py310")
                        bbcTwineUpload(toxenv: "py310", pypi: true)
                        script {
                            env.pypiUpload_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "pypi/upload", status: env.pypiUpload_result)
                        }
                    }
                }
                stage ("Upload to Artifactory") {
                    when {
                        anyOf {
                            expression { return params.FORCE_PYUPLOAD }
                            expression {
                                bbcShouldUploadArtifacts(branches: ["dev"])
                            }
                        }
                    }
                    steps {
                        script {
                            env.artifactoryUpload_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "artifactory/upload", status: "PENDING")
                        sh 'rm -rf dist/*'
                        withBBCRDPythonArtifactory {
                            bbcMakeGlobalWheel("py310")
                        }
                        bbcTwineUpload(toxenv: "py310", pypi: false)
                        script {
                            env.artifactoryUpload_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "artifactory/upload", status: env.artifactoryUpload_result)
                        }
                    }
                }
                stage ("Upload deb") {
                    when {
                        anyOf {
                            expression { return params.FORCE_DEBUPLOAD }
                            expression {
                                bbcShouldUploadArtifacts(branches: ["main"])
                            }
                        }
                    }
                    steps {
                        script {
                            env.debUpload_result = "FAILURE"
                        }
                        bbcGithubNotify(context: "deb/upload", status: "PENDING")
                        script {
                            for (def dist in bbcGetSupportedUbuntuVersions(exclude: ["xenial"])) {
                                bbcDebUpload(sourceFiles: "_result/${dist}-amd64/*",
                                                removePrefix: "_result/${dist}-amd64",
                                                dist: "${dist}",
                                                apt_repo: "ap/python")
                            }
                        }
                        script {
                            env.debUpload_result = "SUCCESS" // This will only run if the steps above succeeded
                        }
                    }
                    post {
                        always {
                            bbcGithubNotify(context: "deb/upload", status: env.debUpload_result)
                        }
                    }
                }
            }
        }
    }
    post {
        always {
            bbcSlackNotify(channel: "#apmm-cloudfit")
        }
    }
}
