import os
from translate import Translator

def contains_cjk(text):
    # Function to check if the text contains any CJK (Chinese, Japanese, Korean) characters
    for character in text:
        if '\u4e00' <= character <= '\u9fff' or \
           '\u3040' <= character <= '\u30ff' or \
           '\u3400' <= character <= '\u4DBF' or \
           '\u20000' <= character <= '\u2A6DF' or \
           '\u2A700' <= character <= '\u2B73F' or \
           '\u2B740' <= character <= '\u2B81F' or \
           '\u2B820' <= character <= '\u2CEAF' or \
           '\uF900' <= character <= '\uFAFF' or \
           '\u2F800' <= character <= '\u2FA1F':
            return True
    return False

def translate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if contains_cjk(content):
        translator= Translator(to_lang="en")
        translated = translator.translate(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(translated)
        print(f"Translated file: {file_path}")

def main(folder_path):
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):  # Assuming you want to translate text files
                file_path = os.path.join(subdir, file)
                translate_file(file_path)

if __name__ == "__main__":
    folder_path = "./fastxgpt"  # Replace with your folder path
    main(folder_path)
