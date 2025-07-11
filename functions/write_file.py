import os

def write_file(working_directory, file_path, content):
    if working_directory is not None and file_path is not None:
        root_path = os.path.abspath(working_directory)
        joined_path = os.path.abspath(os.path.join(root_path, file_path))
    else:
        return f"Error: Missing working_directory or file_path."

    if not joined_path.startswith(root_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        new_dirs = os.path.dirname(joined_path)
        if not os.path.exists(new_dirs):
            os.makedirs(new_dirs, exist_ok=True)

        with open(joined_path, "w") as f:
            f.write(content)


        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"