import os, subprocess

def run_python_file(working_directory, file_path):
    if working_directory is not None and file_path is not None:
        root_path = os.path.abspath(working_directory)
        joined_path = os.path.abspath(os.path.join(root_path, file_path))
    else:
        return f"Error: Missing working_directory or file_path."

    if not joined_path.startswith(root_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(joined_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        sub = subprocess.run(["python3", f"{joined_path}"],timeout=30, text=True, capture_output=True)
        formatter = ""
        formatter += f"STDOUT: {sub.stdout}\n"
        formatter += f"STDERR: {sub.stderr}\n"
        if sub.returncode != 0:
            formatter += f"Process exited with code {sub.returncode}\n"
        if sub.stdout == "":
            formatter += "No output produced.\n"
        return formatter
    except Exception as e:
        return f"Error: executing Python file: {e}"