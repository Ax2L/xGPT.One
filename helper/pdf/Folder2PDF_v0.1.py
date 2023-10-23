#!/usr/bin/env python3
import os
import sys
import time
import configparser
from fpdf import FPDF

# Function to print a nice header and instructions
def print_header():
    print("=================================================")
    print("                      Folder2PDF                 ")
    print("=================================================")
    print("This script takes a directory and generates a PDF summary.")
    print("Run it as follows:")
    print("python script.py /path/to/your/folder /path/to/destination/file.pdf")
    print("=================================================")

# Function to print a dynamic status bar
def print_status_bar(current, total):
    bar_length = 50
    progress = float(current) / float(total)
    arrow = '-' * int(round(progress * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f'\r[{arrow}{spaces}] {current}/{total} files processed.  ')
    sys.stdout.flush()

# Function to generate the directory tree
def generate_tree(directory, padding: str = "", ignored_folders=None):
    if ignored_folders is None:
        ignored_folders = []
        
    if any(ignored in directory for ignored in ignored_folders):
        return ""
    
    tree_str = f"{padding}{os.path.basename(directory)}\n"
    for entry in os.scandir(directory):
        if entry.is_dir() and not any(ignored in entry.path for ignored in ignored_folders):
            tree_str += generate_tree(entry.path, padding + "----", ignored_folders)
        elif entry.is_file():
            tree_str += f"{padding}----{entry.name}\n"
    return tree_str


# Function to read configuration settings from config.ini
def read_config(config_file):
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        return {
            'common_exts': config.get('CommonFileTypes', 'All').split(','),
            'font_size': config.getint('PDFSettings', 'FontSize'),
            'font': config.get('PDFSettings', 'Font'),
            'encoding': config.get('PDFSettings', 'Encoding'),
            'content_limit': config.getint('PDFSettings', 'ContentLimit'),
            'ignored_folders': config.get('Filter', 'IgnoredFolders').split(','),
            'ignored_files': config.get('Filter', 'IgnoredFiles').split(',')
        }
    except configparser.Error as e:
        print(f"Failed to read config.ini: {e}")
        sys.exit(1)

# Function to sanitize text for latin-1 encoding
def sanitize_text_for_latin1(text):
    return ''.join(c for c in text if ord(c) in range(256))

# Function to add content to a PDF page
def write_pdf(pdf, text, font_size, font, title=None):
    pdf.add_page()
    if title:
        pdf.set_font(font, style='B', size=16)
        pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.set_font(font, size=font_size)
    pdf.multi_cell(0, 10, txt=text)

# Main function
def main(directory, destination_file, config):
    print_header()
    pdf = FPDF()
    error_messages = []
    
    # Generate and add the directory tree to the PDF
    tree_str = generate_tree(directory, ignored_folders=config['ignored_folders'])
    write_pdf(pdf, sanitize_text_for_latin1(tree_str), config['font_size'], config['font'], title="Directory Tree")

    total_files = sum([len(files) for _, _, files in os.walk(directory) if not any(ignored in _ for ignored in config['ignored_folders'])])
    processed_files = 0

    for root, dirs, files in os.walk(directory):
        # Filter out directories to be ignored
        if any(ignored_word in root for ignored_word in config['ignored_folders']):
            continue
        # Filter out files to be ignored
        files = [f for f in files if not any(ignored_word in f for ignored_word in config['ignored_files'])]

        relative_root = os.path.relpath(root, directory)
        write_pdf(pdf, sanitize_text_for_latin1(f"Directory: {relative_root}"), config['font_size'], config['font'], title="Folder Structure")
        
        # Filter out files to be ignored and not in common_exts
        files = [f for f in files if not any(ignored_word in f for ignored_word in config['ignored_files']) and any(ext in f for ext in config['common_exts'])]
        
        for file in files:
            processed_files += 1
            print_status_bar(processed_files, total_files)
            
            try:
                file_path = os.path.join(root, file)
                ext = os.path.splitext(file)[-1].lower()[1:]  
                meta_info = f"Size: {os.path.getsize(file_path)} bytes"
                snippet = ""

                with open(file_path, 'r', encoding=config['encoding'], errors='ignore') as f:
                    content = f.read()  # Read the entire file
                    
                    if len(content) > config['content_limit']:  # Apply the limit
                        content = content[:config['content_limit']] + "..."
                        
                info_text = f"File: {file}\nType: {ext.upper() if ext else 'Unknown'}\n{meta_info}"
                
                # Add file content to info_text
                info_text += f"\nContent:\n```{ext}\n{content}\n```"
                
                sanitized_text = sanitize_text_for_latin1(info_text)
                write_pdf(pdf, sanitized_text, config['font_size'], config['font'], title="File Info")
                
            except Exception as e:
                error_messages.append(f"Error processing file {file}: {str(e)}")
                continue

    pdf.output(name=destination_file, dest='F')
    print("\nPDF generation complete.")

    if error_messages:
        with open("folder.pdf.errors.txt", "w") as f:
            f.write("\n".join(error_messages))
        print(f"Errors were encountered. Check folder.pdf.errors.txt for details.")

# Entry point
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory_path> <destination_file>")
        sys.exit(1)

    directory = sys.argv[1]
    destination_file = sys.argv[2]
    config = read_config("config.ini")
    main(directory, destination_file, config)
