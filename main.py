from flask import Flask, jsonify , request
app = Flask(__name__)
import os, shutil, json

from datetime import datetime

def scan_directory(path):
    """
    Recursively scans the given directory path and returns a dictionary representing
    the folder and file structure.
    """
    folder_structure = []
    try:
        for entry in os.scandir(path):
            if entry.is_dir():
                # If the entry is a directory, recursively scan it
                folder_structure.append({
                    'id': entry.inode(),  # Unique ID for each entry
                    'name': entry.name,
                    'type': 'folder',
                    'contents': scan_directory(entry.path)
                })
            else:
                # If the entry is a file, add it to the list
                folder_structure.append({
                    'id': entry.inode(),  # Unique ID for each entry
                    'name': entry.name,
                    'type': 'file'
                })
    except PermissionError:
        pass  # Ignore directories for which permission is denied
    return folder_structure

@app.route('/api/folder-structure', methods=['GET'])
def get_folder_structure():
    """
    Endpoint to get the folder and file structure of the /topic directory.
    """
    base_path = os.path.join(os.getcwd(), 'topic')  # Assuming the /topic folder is in the current working directory
    folder_structure = scan_directory(base_path)
    return jsonify(folder_structure )

def full_path(base, name): return os.path.join(base, name)

def file_manager(ops, base=os.getcwd()):
    for op in ops:
        for cmd, args in op.items():
            try:
                if cmd == "cd": base = args
                elif cmd == "create_folder": os.makedirs(full_path(base, args), exist_ok=True)
                elif cmd == "delete_folder": shutil.rmtree(full_path(base, args))
                elif cmd == "create_file": open(full_path(base, args[0]), 'w').write(args[1] if len(args) > 1 else "")
                elif cmd == "delete_file": os.remove(full_path(base, args))
                elif cmd == "rename": os.rename(full_path(base, args[0]), full_path(base, args[1]))
                elif cmd == "move": shutil.move(full_path(base, args[0]), args[1])
                elif cmd == "update_file": p = full_path(base, args[0]); open(p, 'w').write(args[1]) if os.path.exists(p) and open(p).read() != args[1] else None
                elif cmd == "update_timestamp": p = full_path(base, args); os.utime(p, (datetime.now().timestamp(),)*2) if os.path.exists(p) else None
            except Exception as e:
                print(f"Error with {cmd}: {e}")

# Example usage
operations = [
    {"cd": "/folder"}, {"create_file": ["test.txt", "This is a test file."]},
    {"update_file": ["test.txt", "Updated content."]}, {"rename": ["test.txt", "renamed_test.txt"]},
    {"move": ["renamed_test.txt", "/new_folder"]}, {"create_folder": "another_folder"},
    {"delete_file": "some_file.txt"}, {"delete_folder": "old_folder"}, {"update_timestamp": "renamed_test.txt"}
]

file_manager(operations)
def full_path(base, name): return os.path.join(base, name)

@app.route('/')
def home():
    return "Welcome to Flask!"

@app.post('/costumber/topic') 
def costumber():
    r=request.get_json() 
    try:
        file_manager(r)
        return "true"
    except:
        return "false"
if __name__ == '__main__':
    app.run(debug=True)