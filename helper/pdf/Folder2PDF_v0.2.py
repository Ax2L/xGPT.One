# Folder2PDF.py
#!/usr/bin/env python3
import os
import sys
import configparser
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table


# Function to print a nice header and instructions
def print_header():
    print("=================================================")
    print("                      Folder2PDF                 ")
    print("=================================================")


# [CommonFileTypes]
All = "html","css","js","json","xml","php","ts","yml","yaml","sh","Dockerfile","md","ini","py","gitignore","env"

# [PDFSettings]
FontSize = 12
Font = "Arial"
Encoding = "latin-1"
ContentLimit = 1000

# [Filter]
IgnoredFolders = "node_modules", ".git", "__pycache__"
IgnoredFiles = ".DS_Store", ".gitignore", ".gz"




# Function to read configuration settings from config.ini
def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        'content_limit': 1000,
        'ignored_folders': config.get(IgnoredFolders).split(','),
        'ignored_files': config.get(IgnoredFiles).split(',')
    }

# Function to generate the directory tree
def generate_tree(directory, padding: str = "|--", ignored_folders=None):
    if ignored_folders is None:
        ignored_folders = []

    if any(ignored in directory for ignored in ignored_folders):
        return ""
    
    tree_str = f"{padding}{os.path.basename(directory)}\n"
    for entry in os.scandir(directory):
        if entry.is_dir() and not any(ignored in entry.path for ignored in ignored_folders):
            tree_str += generate_tree(entry.path, padding + "  |--", ignored_folders)
        elif entry.is_file():
            tree_str += f"{padding}  |--{entry.name}\n"
    return tree_str

# Function to write PDF
def write_pdf(directory, destination_file):
    styles = getSampleStyleSheet()
    content = []
    content.append(Paragraph("Folder2PDF Report", styles['Title']))
    content.append(Spacer(1, 12))

    tree_str = generate_tree(directory, ignored_folders=IgnoredFolders)
    content.append(Paragraph("Directory Structure:", styles['Heading2']))
    content.append(Paragraph(tree_str, styles['BodyText']))

    # Add your table, images or other elements here.
    # ...
    
    pdf = SimpleDocTemplate(destination_file, pagesize=letter)
    pdf.build(content)

# Main function
def main(directory, destination_file):
    print_header()
    write_pdf(directory, destination_file)

# Entry point
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory_path> <destination_file>")
        sys.exit(1)

    directory = sys.argv[1]
    destination_file = sys.argv[2]
    main(directory, destination_file)
