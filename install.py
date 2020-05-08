import os
import sys

shell_path = str(os.popen("echo $SHELL"))
shell = shell_path.split("/")[len(shell_path.split("/"))-1]
already_installed = True if not os.popen("markdown -h") == "" else False
if already_installed:
    print("start-markdown is already installed")
    sys.exit()
else:
    if shell == "zsh":
        shell_config_file = os.popen("locate .zshrc")
    elif shell == "bash":
        shell_config_file = os.popen("locate .bashrc")
    else:
        print("Your current default shell is not yet supported")
        print(f"Please add markdown={os.getcwd()}/mardown.py to your shell's rc file manually.")
        sys.exit()

    if not shell_config_file == "":
        os.system(f"echo 'markdown=$(pwd)/markdown.py' >> {shell_config_file}")
        sys.exit()
    else:
        print("An error occured")
        print(f"Please add markdown={os.getcwd()}/mardown.py to your shell's rc file manually.")
        sys.exit()