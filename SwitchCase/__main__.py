 
from re import split as spl

def ded():
    print("double ded")

class switch:

    command_list = []
    code_count   = 1

    def __init__(self, 
                 code=None, 
                 value=None):

        if value is not None:
            if type(value) == str:
                if not value.startswith('"'):
                    value = '"' + value
                if not value.endswith('"'):
                    value += '"'

        self.code  = code 
        self.value = value
        
        if code is not None:
            if type(code) != str:
                raise ValueError("Ensure you are inputting a string into this class!")
            
            self._proccess_lines()
            self._proccess_commands()
            self._clear_vars()

    def case(self, code: str):

        self.code_count += 1
        self.code        = code 

        self._proccess_lines()
        self._proccess_commands()
        self._clear_vars()

    def _clear_vars(self):

        self.command_list.clear()
        self.code = ""

    def _proccess_commands(self):

        for command in self.command_list:
            try: exec(command)
            except Exception as e:
                raise SyntaxError(str(e))

    def _proccess_lines(self):

        refined_case      = self.code.split("\n")
        in_case           = False 
        in_valid_case     = False 
        found_valid_case  = False 

        for line_number, line in enumerate(refined_case):

            if line.isspace() or line == "": continue 
            elif line.startswith("#"):       continue 

            elif line.startswith("switch"):

                switch_lines = line.split(" ")
                for item in switch_lines:
                    if item is None: switch_lines.remove(None)
                    elif item.isspace() or item == "":
                        switch_lines.remove(item)

                try: self.value = switch_lines[1].replace("(", "").replace("):", "")
                except IndexError: raise SyntaxError(f"Syntax error at line {line_number + 1}! Follow this format: `switch (value):`")
            
            elif line.startswith("case"):

                in_case    = True 
                case_lines = spl(" |:", line)

                if str(case_lines[1]) == str(self.value):
                    
                    found_valid_case = True 
                    in_valid_case    = True 
                    if case_lines[2].isspace() or case_lines[2] == '':
                        try: command = case_lines[3]
                        except: continue  
                    else: command = case_lines[2]

                    self.command_list.append(command)

                elif str(case_lines[1]) == "default":
                    
                    if found_valid_case:  
                        in_valid_case = False
                        continue 

                    in_valid_case = True 
                    if case_lines[2].isspace() or case_lines[2] == '':
                        try: command = case_lines[3]
                        except: continue  
                    else: command = case_lines[2]

                    self.command_list.append(command)

                else:
                    in_valid_case = False
            
            else:

                if   not in_case:       raise SyntaxError(f"Syntax error at line {line_number + 1}!")
                elif not in_valid_case: continue 
                self.command_list.append(line.lstrip())

        return None

case = """

switch (2):

case 1: 
    print("ok")

case 2: print("ded")
    print("ded")

case "oh":
    # print('get syntax errored bro')
    ded()

case default:
    print("default case - catches everything else")
"""

case2 = """

switch (2):

case 1:
    print("fxc is a hoe")

case default:
    print("E")
"""

switch1 = switch(value=2)
switch1.case(code=case)
switch1.case(code=case2)
