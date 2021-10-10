#!/usr/bin/python3
"""
A script to automatically change french python
keywords into english python keywords. Don't ask.

Copyright (c) 2021 Mrmagicpie 
"""

import sys

try:
    filename = sys.argv[1]
except IndexError as exc:
    raise SystemExit("Please provide a filename!") from exc

runfile = False
hide_contents = False  

try:
    second = sys.argv[2]
    
    if second in {"y", "yes"}:
        runfile = True 
    elif second in {"hide"}:
        hide_contents = True 
    else:
        raise SystemExit(f"Unknown option: {second}")

    del second 
except IndexError:
    pass 

script = open(filename, 'r', encoding='utf-8')
new_filename = filename.replace(".py", "_en_fr.py")
keywords = {
    # These have to be in this order to prevent replacing 
    # items in other items, and causing syntax errors 
    "asynchrone": "async",
    "ausi": "elif",
    "pass": "passe",
    "pour": "for",
    "retour": "return",
    "rendement": "yield",

    "si": "if",
    "ou": "or",
    "de": "from",
    "et": "and",
    "ne": "not",
    " pas": "",  # This allows us to do `si ne Vrai pas` and `si ne Vrai` which means `if not True` 


    # The order doesn't matter on these
    "avec": "with",
    "tantque": "while",
    "essayer": "try",
    "lancer": "raise",
    "est": "is",
    "importer": "import",
    "globale": "global",
    "enfin": "finally",
    "sauf": "except",
    "else": "autre",
    "eff": "del",
    "continuer": "continue",
    "classe": "class",
    "affirmer": "assert",
    "comme": "as",
    "Rien": "None",
    "dans": "in",
    "déf": "def",
    "Vrai": "True",
    "Faux": "False",
    "attendre": "await",
    "pause": "break"

    # "nonlocale": "nonlocal",
    # "nonlocal": "nonlocal",  # Same in both languages
    # "global": "global",  # Same in both languages
    # "pas": "not",
    # "lambda": "lambda",
}

line_number = 0 
new_file = []
module_docstring = ""
in_module_docstring = False 
in_multiline_comment = False 

for line in script.readlines():

    line_number += 1

    if line.isspace() or line.startswith("#"):
        continue

    line = line.rstrip("\n")

    redone_line = None 
    indentation = ""
    
    if not in_multiline_comment:
        if line.startswith('"""'):
            if line.endswith('"""') and (line.count('"') >= 6):
                module_docstring = (line + "\n")
                continue 
            if line_number == 1:
                in_module_docstring = True 
                module_docstring = (line + "\n") 
            in_multiline_comment = True
            continue 
    else:
        if in_module_docstring:
            module_docstring += (line + "\n")  

        if line.startswith('"""') or line.endswith('"""'):
            in_module_docstring  = False 
            in_multiline_comment = False
        continue 

    tries = 0 
    iterations = 0

    def append_line():
        new_file.append(
            ((indentation or "") + use_line + f"  # Line: {line_number}")
        )

    while True:
        try:
            if iterations > 2:
                break 

            use_line = (redone_line or line)
            iterations += 1

            if line.strip().startswith("#"):
                break 

            compile(use_line, filename, 'exec')
            append_line()
            break

        except IndentationError:
            use_line = ""
            found_text = False 
            
            for space in list(line):
                if space.isspace() and not found_text:
                    indentation += space
                else:
                    found_text = True 
                    use_line += space 
            redone_line = use_line

        except SyntaxError as exc:
            if str(exc).startswith("unexpected EOF while parsing"):
                append_line()
                break 

            if tries:
                raise SyntaxError("We can't fix this!") from exc
            tries += 1
            for keyword, replacement in keywords.items():
                redone_line = (redone_line or line).replace(keyword, replacement)

with open(new_filename, "w", encoding="utf-8") as file:
    if module_docstring:
        new_new_file = [module_docstring]
        new_new_file.extend(new_file)
        new_file = new_new_file
    contents = '\n'.join(new_file)
    
    if not hide_contents and not runfile:
        print("writing to file\n---------------")
        print(contents)

    file.write(contents)  # Yes I tried `writelines` but it errored so shut

if runfile:
    exec(open(new_filename).read())
