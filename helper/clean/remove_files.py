import os

def delete_files(target_directory, names_to_delete):
    for root, dirs, files in os.walk(target_directory):
        for file in files:
            # Check if the file name (without extension) is in the list of names to delete
            if os.path.splitext(file)[0] in names_to_delete:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f'Deleted: {file_path}')
                except Exception as e:
                    print(f'Failed to delete {file_path}: {e}')

# Specify the directory to search
target_directory = '.'

# Specify the list of names to delete (without extensions)
names_to_delete = ['DS_Store', '.DS_Store']

# Call the function
delete_files(target_directory, names_to_delete)
