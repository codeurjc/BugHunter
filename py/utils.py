import os

def createDirIfNotExist(folder_name):
    if not os.path.isdir(folder_name): 
        os.makedirs(folder_name)
        return True
    return False

def replaceInFile(file_path, original, new):

    with open(file_path, "rt") as fd:
        data = fd.read()
        data = data.replace(original, new)
        
    with open(file_path, "wt") as fd: 
        fd.write(data)

if __name__ == "__main__":
    replaceInFile("configFiles/_mavenConfig/settings.xml", "/usr/share/maven/ref/repository", "/root/.m2/")