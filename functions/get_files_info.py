import os

def get_files_info(working_directory, directory=None):

    if working_directory is not None:
        root_path = os.path.abspath(working_directory)
        joined_path = root_path
        if directory is not None:
            joined_path = os.path.abspath(os.path.join(root_path, directory))
    else:
        return f"Error: Missing working_directory."

    if not joined_path.startswith(root_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if os.path.isdir(joined_path) != True:
        return f'Error: "{directory}" is not a directory'
    
    try:
        dir_items = os.listdir(joined_path)
        dir_info = ""

        for item in dir_items:
            item_path = os.path.join(joined_path, item)
            dir_info += f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n"
                
        return dir_info
    
    except Exception as e:
         return f"Error: {e}"