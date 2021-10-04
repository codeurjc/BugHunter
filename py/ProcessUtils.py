import subprocess
import os
import sys

class ProcessManager():

    def __init__(self, output, log_name="PROCESS MANAGER"):
        self.outfile = output
        self.log_name = log_name

    @staticmethod
    def default_exec(command, output=None, returnOutput=False):
        dpm = ProcessManager(open("default.log", 'w'), "DEFAULT PROCESS MANAGER")
        exit_code, text = dpm.execute(command, output, returnOutput)
        dpm.close()

    def execute(self, command, output=None, returnOutput=False):
        
        if returnOutput:
            with open('/tmp/run', 'w+') as out:
                exit_code, _ = self.execute(command, output=out)
            with open('/tmp/run', 'r+', errors='ignore') as out:
                text = out.read()
            self.execute("rm /tmp/run")
            return exit_code, text
        else:
            if output is None:
                output=self.outfile
            exit_code = subprocess.call(command, shell=True, stdout=output, stderr=output)
            return exit_code, None

    def log(self, message, output=None):
        if output is None:
            output=self.outfile
        subprocess.call("echo [ %s ] %s"%(self.log_name, message), shell=True, stdout=output, stderr=output)

    def close(self):
        if self.outfile is not None:
            self.outfile.close()