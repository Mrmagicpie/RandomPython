
from typing import Union as U 
from re     import split as spl

class switch:
    def __init__(self, value, case, **args):

        if type(case) != str:
            raise ValueError("Ensure you are inputting a string into this class!")
        
        self.code_count   = 1
        self.case         = case 
        self.value        = value 
        self.command_list = []
        
        self._proccess_lines()
        self._proccess_commands()

        return None

    def _proccess_commands(self):

        for command in self.command_list:
            try: exec(command)
            except Exception as e:
                raise SyntaxError(str(e))

    def _proccess_lines(self):

        self.refined_case = self.case.split("\n")
        in_case           = False 
        in_valid_case     = False 
        found_valid_case  = False 

        for line_number, line in enumerate(self.refined_case):

            if line.isspace() or line == "": continue 
            elif line.startswith("#"):       continue 

            elif line.startswith("switch"):

                switch_lines = line.split(" ")
                for item in switch_lines:
                    if item is None: switch_lines.remove(None)
                    elif item.isspace() or item == "":
                        switch_lines.remove(item)

                self.value = switch_lines[1].replace("(", "").replace("):", "")

            
            elif line.startswith("case"):

                in_case    = True 
                case_lines = spl(" |:", line)

                if str(self.value) == str(case_lines[1]):
                    
                    in_valid_case = True 
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
                if   not in_case: raise SyntaxError(f"Syntax error at line {line_number + 1}!")
                elif not in_valid_case: continue 
                self.command_list.append(line)

        return None


case = """
switch ("oh"):
case 1: 
print("ok")
case 2: print("ded")
print("ded")
case "oh":
print('get syntax errored bro')
ded
case default:
print("default case - catches everything else")
"""

switch(value=2, case=case)
