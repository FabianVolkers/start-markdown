#!/usr/bin/env python3
import os
import sys
import re

class TooManyArgumentsException(Exception):
    def __init__(self):
        super.__init__(self)

class InvalidFileNameException(Exception):
    def __init__(self):
        super.__init__(self)

class FileCreationError(Exception):
    def __init__(self):
        super.__init__(self)

HELP_TEXT = """
Markdown Document Creator

Usage: markdown [options] [filename]

FLAGS:
-h, --help\t Display this help text
-f, --force\t Force overwrite if file exists
-o, --open\t Open file in VSCode after creation

"""

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
    if len(argv) == 1:
        return "", ""
    elif len(argv) == 2:
        if argv[1][0] == "-":
            return argv[1], ""
        else:
            return "", argv[1]
    elif len(argv) == 3:
        if argv[1][0] == "-":
            return argv[1], argv[2]
        else:
            return argv[2], argv[1]
    else:
        raise TooManyArgumentsException


def get_path(filename):

    FULL_PATHS = ["/", "~", "."]
    if filename[0] in FULL_PATHS :
        path = filename
    else:
        current_directory = os.getcwd()
        path = f"{current_directory}/{filename}"
    
    return path

def evaluate_options(options):
    evaluated_options = {
        'overwrite': None,
        'open': False,
    }
    if options == "--help" or options == "-h":
        print(HELP_TEXT)
        sys.exit()
    elif options == "--force" or options == "-f":
        evaluated_options['overwrite'] = True
    elif options == "--open" or options == "-o":
        evaluated_options['open'] = True
    elif options == "-fo" or options == "-of":
        evaluated_options['overwrite'] = True
        evaluated_options['open'] = True
    
    return evaluated_options

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

def open_document(path):
    
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

    try:
        options, filename = read_arguments(sys.argv)
        evaluated_options = evaluate_options(options)
        document_created = False
        
        filename, title = evaluate_filename(filename)

        path = get_path(filename)
        try:
            document_created = create_document(title, path, evaluated_options['overwrite'])

        except FileExistsError:
            if evaluated_options['overwrite'] == None:
                overwrite = input(f"The file you are trying to create already exists. Do you want to overwrite the file {path}? y|n\n")
                evaluated_options['overwrite'] = confirm_action(overwrite)
                try:
                    document_created = create_document(title, path, evaluated_options['overwrite'])
                except FileExistsError:
                    print(f"File {path} exists and will not be overwritten.")
                    sys.exit()
            else:
                print(f"File {path} exists and will not be overwritten.")
                sys.exit()

        finally:
            if evaluated_options['open'] and document_created:
                open_document(path)
                sys.exit()

    except TooManyArgumentsException:
        print("Too many arguments provided, aborting program.")
        print(HELP_TEXT)
        sys.exit()
    except InvalidFileNameException:
        print(f"{filename} is not a valid filename.")
        print(f"Filenames have to match this regular expression {VALID_FILENAME}")
        sys.exit()
    except PermissionError:
        print("Permission denied.")
        sys.exit()
        
    


