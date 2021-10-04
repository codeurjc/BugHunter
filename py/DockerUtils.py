# import subprocess
# import re
import os
# import sys
import docker

DEFAULT_TIMEOUT=1200

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

    def execute(self, docker_image, container_name, command, workdir="/"):
        
        if not self.container_exist(container_name):
            # NOT EXISTS -> CREATE
            container = self.client.containers.run(docker_image,"tail -f /dev/null",
                name=container_name, 
                detach=True,
                volumes_from=[os.environ['HOSTNAME']],
                working_dir=workdir,
                auto_remove=True
            )
            self.containers.append(container)
        else:
            container = self.client.containers.get(container_name)
        
        (exit_code, container_output) = container.exec_run("timeout %d bash -c '%s'"%(DEFAULT_TIMEOUT,command))
        return exit_code, container_output

if __name__ == "__main__":

    dockerUtils = DockerClient()

    exit_code, container_output = dockerUtils.execute("defects4j:2.0.0", "defects4j-container", "defects4j info -p JacksonDatabind -b 1")
    print(container_output)
