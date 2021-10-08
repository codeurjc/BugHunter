import subprocess
from injectable import injectable

@injectable(singleton=True)
class ProcessManager():

    def __init__(self):
        self.log_name = "PROCESS MANAGER"
        self.outfile = open("/tmp/process-manager.log", 'w+')

    def setNewOutput(self, output, log_name):
        self.log_name = log_name
        self.outfile = open(output, 'w+')

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

    def log(self, message, output=None, log_prefix=None):
        if log_prefix is None: log_prefix = self.log_name
        if output is None:
            output=self.outfile
        subprocess.call("echo [ %s ] %s"%(log_prefix, message), shell=True, stdout=output, stderr=output)

    def close(self):
        if self.outfile is not None:
            self.outfile.close()