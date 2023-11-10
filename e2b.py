#!/usr/bin/env python3
"""e2b: a simple python script that converts Evernote note links and colored text to Bear note links and highlighted markdown text"""
import os
import re

def input_enex_path():
    """Read .enex files in directory.
    ---
    - Accept path to directory from user input
    - Verify that directory is valid with os.path.exists()
    - Scan directory with os.scandir and create files object
    - Create directory for converted files
    - Run function to convert Evernote note links and colored text to Bear note links and highlighted text in each file
    """
    path = input("Please input the path to a directory with Evernote exports: ")
    if not os.path.exists(path):
        print(f"Not a valid file path:\n{path}")
        return
    else:
        print(f"Valid file path: {path}")
    if not os.path.exists(f"{path}/bear"):
        os.mkdir(f"{path}/bear")
    for file in os.scandir(path):
        if file.is_file() and file.name.endswith(".enex"):
            convert_links(file)

def convert_links(file):
    """convert Evernote note links and colored text to Bear note links and highlighted markdown text.
    ---
    - Replace Evernote note link URIs, but not other URIs, with Bear note links
    - Replace colored text from Evernote with Highlighted text in Bear Note
    - Write to a new file in the bear subdirectory
    """
    try:
        print(f"Converting {file.name}...")
        with open(file) as enex:
            content = enex.read()
            # the re.sub expression below converts evernote wiki links to Bear note wiki links by replacing all evernote:/// links with the actual name of the evernote note wrapped in [[ ]]
            content = re.sub(r'(<a[^>]*?href="evernote[^>]*?>)(.*?)(</a>?)', r"[[\2]]", content)
            # the re.sub expression below escapes all "/" found between [[ ]] by replaceing them with "\/" (which is neccessary because otherwise Bear creates a new note when the wiki is clicked)
            content = re.sub(r'\[\[[^\]]*\/[^\]]*\]\]', lambda x: x.group().replace('/', '\\/'), content) 
            # the re.sub expression below turns ALL colored text into highlighted text in bear by wrapping the text in == * ==
            #content = re.sub(r'(<span style="color:rgb[^>]*?>\s*)(.*?)(\s*</span>?)', r"==\2==", content)
            # the re.sub expression below turns green (rgb 24, 168, 65) colored text into highlighted text in bear by wrapping the text in "== * =="
            #content = re.sub(r'(<span style="color:rgb\(24, 168, 65\);--inversion-type-color:simple;">\s*)(.*?)(\s*</span>?)', r"==\2==", content)
            # the re.sub expression below turns purple (rgb 182, 41, 212) colored text into highlighted and underlined text in bear by wrapping the text in "==~ * ~=="
            #content = re.sub(r'(<span style="color:rgb\(182, 41, 212\);--inversion-type-color:simple;">\s*)(.*?)(\s*</span>?)', r"==~\2~==", content)
            with open(f"{os.path.dirname(file)}/bear/{file.name}", "x") as new_enex:
                new_enex.write(content)
            print("Done. New file available in the bear subdirectory.")
    except Exception as e:
        print(f"An error occurred:\n{e}\nPlease try again.")

if __name__ == "__main__":
    input_enex_path()
