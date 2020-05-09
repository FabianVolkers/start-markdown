
# Markdown Document Creator <!-- omit in TOC -->

A python script for generating markdown documents with a table of contents recognised by the [Markdown All in One VSCode Extension](https://marketplace.visualstudio.com/items?itemName=yzhang.markdown-all-in-one)

## Contents <!-- omit in TOC -->
- [Template](#template)
- [Usage](#usage)
- [Installation](#installation)
  - [Manually install script](#manually-install-script)
  - [Using setup.py](#using-setuppy)

## Template
The python script will generate a markdown documents according to this template. The title will be replaced by the document name without the `.md` extension.
```markdown
# {Title} <!-- omit in TOC -->

## Contents <!-- omit in TOC -->
- [Section 1](#section-1)

## Section 1
```

## Usage
```bash
Markdown Document Creator

Usage: markdown [options] [filename]

FLAGS:
-h, --help\t Display this help text
-f, --force\t Force overwrite if file exists
-o, --open\t Open file in VSCode after creation
```

## Installation

### Manually install script
```zsh
git clone https://github.com/FabianVolkers/start-markdown.git
cd start-markdown
chmod 744 markdown.py
cp markdown.py /usr/local/bin/markdown
# For zsh
echo "markdown=/usr/local/bin/markdown" >> ~/.zshrc
# For bash
echo "markdown=/usr/local/bin/markdown" >> ~/.bashrc
```
### Using setup.py
```zsh
git clone https://github.com/FabianVolkers/start-markdown.git
cd start-markdown
python3 setup.py
```
