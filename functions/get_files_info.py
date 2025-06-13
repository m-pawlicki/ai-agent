import os

def get_files_info(working_directory, directory=None):
        if directory not in  os.listdir(path=working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(directory) != True:
            return f'Error: "{directory}" is not a directory'