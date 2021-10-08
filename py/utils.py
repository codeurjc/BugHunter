import os

def createDirIfNotExist(folder_name):
    if not os.path.isdir(folder_name): 
        os.makedirs(folder_name)
        return True
    return False