from utils.style import green
import os


def update_file(path, new_content):
    # Ensure the directory exists; if not, create it
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Write content to the file
    with open(path, 'w') as file:
        file.write(new_content)
        print(green(f"Updated file {path}"))

def get_files_content(directory, ignore=[]):
    return_array = []

    for root, dirs, files in os.walk(directory):
        # Ignore directories
        dirs[:] = [d for d in dirs if d not in ignore]

        for file in files:
            if file in ignore:
                continue

            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                file_content = f.read()

            file_name = os.path.basename(path)
            relative_path = path.replace(directory, '').replace('\\', '/').replace('/' + file_name, '')
            return_array.append({
                'name': file_name,
                'path': relative_path,
                'content': file_content,
                'full_path': path,
            })

    return return_array

def clear_directory(dir_path, ignore=[]):
    for root, dirs, files in os.walk(dir_path, topdown=True):
        # Remove ignored directories from dirs so os.walk doesn't traverse them
        dirs[:] = [d for d in dirs if d not in ignore]

        for file in files:
            if file in ignore:
                continue

            path = os.path.join(root, file)
            os.remove(path)

        # Delete directories not in ignore list
        for d in dirs:
            dir_path = os.path.join(root, d)
            if not os.listdir(dir_path):  # Check if directory is empty
                os.rmdir(dir_path)