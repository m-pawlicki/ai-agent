import os

def get_file_content(working_directory, file_path):
    if working_directory is not None and file_path is not None:
        root_path = os.path.abspath(working_directory)
        joined_path = os.path.abspath(os.path.join(root_path, file_path))
    else:
        return f"Error: Missing working_directory or file_path."
    
    MAX_CHARS = 10000

    if not joined_path.startswith(root_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(joined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(joined_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            
        if os.path.getsize(joined_path) > len(file_content_string):
            file_content_string += f' [...File "{file_path}" truncated at 10000 characters]'

        return file_content_string
    except Exception as e:
        return f"Error: {e}"