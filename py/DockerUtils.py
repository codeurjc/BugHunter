# import subprocess
# import re
import os
# import sys
import docker
import getpass
from injectable import injectable
from utils import replaceInFile

DEFAULT_TIMEOUT=1200

@injectable(singleton=True)
class DockerClient():        

    def __init__(self):
        self.client = docker.from_env()
        self.containers = []

    def container_exist(self, container_name):
        try:
            self.client.containers.get(container_name)
            return True
        except docker.errors.NotFound as e:
            return False

    def shutdownContainers(self):
        for container in self.containers:
            container.stop()
        self.client.close()

    def createVolumeIfNotExist(self, name):
        try:
            self.client.volumes.get(name)
            # Exists
        except docker.errors.NotFound:
            # Not exist -> Create
            self.client.volumes.create(name=name, driver="local")

    def initContainer(self, docker_image, container_name, workdir="/", volumes={}, env={}):
        container = self.client.containers.run(docker_image,"tail -f /dev/null",
                name=container_name, 
                detach=True,
                volumes=volumes,
                volumes_from=[os.environ['HOSTNAME']],
                working_dir=workdir,
                #user=1000,
                auto_remove=True,
                environment=env
            )
        self.containers.append(container)


    def execute(self, container_name, command):
        
        container = self.client.containers.get(container_name)
        
        (exit_code, container_output) = container.exec_run("timeout %d bash -c '%s'"%(DEFAULT_TIMEOUT,command), user="1000")
        return exit_code, container_output

if __name__ == "__main__":

    dockerCli = DockerClient()
    #dockerCli.createVolumeIfNotExist("example-1")
    # m2_path="/home/regseek/workdir/results/SpringBootSamples/Bug_1/libs"
    env = {
            # "MAVEN_CONFIG": m2_path
    }
    dockerCli.initContainer("maven:3-jdk-8-slim", "example", env=env)
    
    # replaceInFile(m2_path+"/settings-docker.xml", "/usr/share/maven/ref/repository", m2_path)