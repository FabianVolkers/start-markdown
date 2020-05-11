#!/usr/bin/env python3
import os
import sys
import re
import argparse

class InvalidFileNameException(Exception):
    def __init__(self):
        super.__init__(self)

class FileCreationError(Exception):
    def __init__(self):
        super.__init__(self)



VALID_FILENAME = re.compile("^[a-zA-Z0-9_\.][a-zA-Z0-9_\.-]{0,256}$")

def confirm_action(response):
    if response == "y" or response == "yes":
        return True

    elif response == "n" or response == "no":
        return False
    else:
        response = input("Please type y or n\n")
        return confirm_action(response)

def create_document(title, path, overwrite):
    content = f"""
# {title} <!-- omit in TOC -->

## Contents <!-- omit in TOC -->
- [Section 1](#section-1)

## Section 1
"""
    if overwrite:
        try:
            with open(path, mode="w") as file:
                file.write(content)
                file.close()
            return True
        except:
            print("error creating file")
            raise FileCreationError


    else:
        try:
            with open(path, mode='x') as file:
                file.write(content)
                file.close()
            return True
        except FileExistsError:
            raise FileExistsError

def read_arguments(argv):
    parser = argparse.ArgumentParser(description='Markdown Document Creator')
    parser.add_argument('filename', help='Filename or Path of the Markdown file to be created')
    parser.add_argument('-f', '--force', action='store_true', help='Force overwrite if file exists')
    parser.add_argument('-o', '--open', action='store_true', help='Open file in preferred editor')
    parser.add_argument('-e', '--editor', help='Choose an editor to open the file with')
    return parser.parse_args(argv)



def get_path(filename):

    FULL_PATHS = ["/", "~", "."]
    if filename[0] in FULL_PATHS :
        path = filename
    else:
        current_directory = os.getcwd()
        path = f"{current_directory}/{filename}"
    
    return path



def evaluate_filename(filename):
    if filename == "":
        filename = input("Please enter a filename\n")

    MARKDOWN_EXTENSION = re.compile("(\.markdown|\.mdown|\.mkdn|\.mkd|\.md)$")
    extension_match = MARKDOWN_EXTENSION.search(filename)
    if extension_match == None:
        title = filename.split("/")[len(filename.split("/"))-1]
        filename = f"{filename}.md"
    else:
        title = filename.split("/")[len(filename.split("/"))-1]
        title = title[:extension_match.start()]

    
    filename_match = VALID_FILENAME.search(filename)
    if filename_match == None:
        raise InvalidFileNameException

    return filename, title

def open_document(path, editor):
    if not editor == None:
        os.system(f"{editor} {path}")
    else:
        code = os.popen("which code")
        editor = os.popen("$EDITOR").read()
        nano = os.popen("which nano")
        vim = os.popen("which vim")

        if not code == "code not found":
            os.system(f"code {path}")
        elif not editor == "":
            os.system(f"$EDITOR {path}")
        elif not nano == "nano not found":
            os.system(f"nano {path}")
        elif not vim == "vim not found":
            os.system(f"vim {path}")
        else:
            print("no editor found. Aborting program without opening file.")
            sys.exit()

if __name__ == "__main__":
    namespace = read_arguments(sys.argv[1:])
    editor = namespace.editor
    filename = namespace.filename
    overwrite = namespace.force
    open_file = namespace.open
    
    try:

        document_created = False
        
        filename, title = evaluate_filename(filename)

        path = get_path(filename)
        document_created = create_document(title, path, overwrite)

    except FileExistsError:
        if overwrite == False:
            overwrite_response = input(f"The file you are trying to create already exists. Do you want to overwrite the file {path}? y|n\n")
            overwrite = confirm_action(overwrite_response)
            try:
                document_created = create_document(title, path, overwrite)
            except FileExistsError:
                print(f"File {path} exists and will not be overwritten.")
                sys.exit()
        else:
            print(f"File {path} exists and will not be overwritten.")
            sys.exit()


    except InvalidFileNameException:
        print(f"{filename} is not a valid filename.")
        print(f"Filenames have to match this regular expression {VALID_FILENAME}")
        sys.exit()

    except PermissionError:
        print("Permission denied.")
        sys.exit()

    finally:
        if open_file and document_created:
            open_document(path, editor)
            sys.exit() 
    
    


