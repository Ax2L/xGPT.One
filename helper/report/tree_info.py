import os

def list_files(startpath, ignore_list):
    for root, dirs, files in os.walk(startpath):
        # Remove directories in ignore_list
        dirs[:] = [d for d in dirs if d not in ignore_list]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        print(f"{indent}{os.path.basename(root)}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        
        for f in files:
            if any(word in f for word in ignore_list):
                continue
            
            print(f"{sub_indent}{f}")

# Keywords to ignore
ignore_list = ['__pycache__', '.pyc', '.git']

# Start from the current directory
list_files('.', ignore_list)
