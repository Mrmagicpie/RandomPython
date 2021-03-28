#
#                            SwitchCase __main__.py | 2021 (c) Mrmagicpie
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
from re     import split    as spl
from typing import Optional as O
#
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class switch:
    """
    The switch class is a python extension written in python. It allows the use 
    of the switch case, syntax similar to those in C#, Bash, Java, etc. 
    """

    # Create some variables to use in the class. 
    # I put them here and not in a self. because 
    # it's easier to read. 
    command_list = []
    code_count   = 1

    def __init__(self, 
                 code      : str  = None, 
                 value     : any  = None,
                 clear_code: bool = True) -> None:
        """
        The switch class is a python extension written in python. It allows the use 
        of the switch case, syntax similar to those in C#, Bash, Java, etc. 
        :param code: Your str code. This is optional as you can use the .case() function to evaulate code.
        :param value: Your switch value. This is also optional because you can specify the value in your code.
        :return: Returns the class.
        """

        # See if the user supplied a predefined value(like a switch statement), 
        # if they did **and** it's a string, we'll add quotes to the begining 
        # and end of the value. This just makes it easier to use it in a string 
        # case. 
        if value is not None:
            if type(value) == str:
                value = self._proccess_str_value(value)

        # Define the global variables, for now.
        self.code  = code 
        self.value = value
        self.clear = clear_code
        
        # If the code is set in the class initialization 
        # we'll see if it's a string and then run it. If 
        # it isn't a string it'll throw a ValueError because
        # I want a string >:(
        if code is not None:
            
            self._proccess_lines()
            self._proccess_commands(process_switch=False if value is not None else True)
            if self.clear: self._clear_vars()

    def case(self, 
             code : str  = None, 
             value: any  = None,
             rerun: bool = False) -> O[RuntimeWarning]:
        """
        Interprete and run your switch case statements.
        :param code: Your multiline string of all your code. 
        :return: Returns whatever your code runs :> 
        """

        # Add one to this class's code count
        self.code_count += 1

        if value is not None:
            if type(value) == str:
                value = self._proccess_str_value(value)
            self.value = value

        # See if the user wants to rerun the code. If
        # there isn't any code to run we'll raise a 
        # RuntimeWarning and let the user know what
        # the problem is!
        if rerun:
            if self.code is None:
                raise RuntimeWarning("You have not supplied any code to rerun!")

            else:
                if len(self.command_list) != 0 and value is None:
                    self._proccess_commands()
                    if self.clear: self._clear_vars()

                elif value is not None:
                    self._proccess_lines(process_switch=False if value is not None else True)
                    self._proccess_commands()
                    if self.clear: self._clear_vars()

                else:
                    raise RuntimeWarning("No code has been rerun because there has been no code processed!")

        # Redefine the code var to be used later on.
        if code is not None:
            self._clear_vars()
            self.code = code 

        # Run the code.
        self._proccess_lines()
        self._proccess_commands()
        if self.clear: self._clear_vars()

    def _clear_vars(self) -> None:
        """
        Internal function to clear variables.
        :return: Empty class vars.
        """

        self.command_list.clear()
        self.code = ""

    def _proccess_str_value(self, value: str) -> str:

        if not value.startswith('"'):
            value = '"' + value

        if not value.endswith('"'):
            value += '"'
        
        return value 

    def _proccess_commands(self) -> O[SyntaxError]:
        """
        Internal function to proccess commands found by the interpreter. 
        :return: Whatever your code is <:
        """

        for command in self.command_list:
            try: exec(command)
            except Exception as e:
                raise SyntaxError(str(e))

    def _proccess_lines(self, process_switch: bool = True) -> None:
        """
        Internal function to process the code given.
        :return: None, SyntaxError, and invoking the :func:_proccess_commands function.
        """

        # Create necessary variables for the interpreter to use later.
        refined_case      = self.code.split("\n")
        in_case           = False 
        in_valid_case     = False 
        found_valid_case  = False 

        # Enumerate over each line to get the line number to be 
        # used in SyntaxErrors and the line for the actual data.
        for line_number, line in enumerate(refined_case):

            # If the line is nothing or a comment we'll ignore it.
            if line.isspace() or line == "": continue 
            elif line.startswith("#"):       continue 

            line = line.lstrip()

            # Our first statement is the Switch! The Switch 
            # statement is used to define what we're comparing. 
            # This can be used to redefine our conditionals at 
            # runtime and to define them if the value arg isn't
            # passed at class initialization.
            if line.startswith("switch"):

                if not process_switch: continue 

                # Attempt to split the switch and then process the 
                # arg into a usable value var. It will throw a 
                # SyntaxError if you didn't do it right!
                switch_lines = line.split(" ")

                # Old code from using re.
                # for item in switch_lines:
                #     if item is None: switch_lines.remove(None)
                #     elif item.isspace() or item == "":
                #         switch_lines.remove(item)

                try: self.value = switch_lines[1].replace("(", "").replace("):", "")
                except IndexError: raise SyntaxError(f"Syntax error at line {line_number + 1}! Follow this format: `switch (value):`")
            

            # Our next statment is the case statement. This works
            # similar to the normal if statement. It will do a 
            # direct comparison to your value with the supplied
            # case arg. Basically arg == value.
            elif line.startswith("case"):

                # Tell the interpreter not to throw a SyntaxError
                # because we are now in a case. And also split
                # the case into usable args.
                in_case    = True 
                case_lines = spl(" |:", line)

                # Now we'll check if our case is the right value,
                # then if it isn't we'll check if the case is the 
                # default case, and then finally, after all that
                # we'll let the interpreter know we're no longer
                # in a valid case.
                if str(case_lines[1]) == str(self.value):
                    
                    # Now we set some variables to let 
                    # the interpreter know what's happening.
                    found_valid_case = True 
                    in_valid_case    = True 

                    # See if the second arg is space or empty,
                    # if it is we'll try to use the third arg 
                    # and if that fails we'll then tell the user 
                    # that their syntax is wrong. 
                    if case_lines[1].isspace() or case_lines[1] == '':
                        try: command = case_lines[2]
                        except: raise SyntaxError(f"Value Case - The interpreter cannot find a case statement at line {line_number + 1}! Follow this format: `case statement:`")  
                    else: command = case_lines[1]

                    # If all that was sucessful we'll add the 
                    # command to the list to be executed soon!
                    self.command_list.append(command)

                elif str(case_lines[1]) == "default":
                    
                    # See if we're already in a valid case 
                    # and if we are then we'll stop that and 
                    # continue with the loop. 
                    if found_valid_case:  
                        in_valid_case = False
                        continue 

                    in_valid_case = True 

                    # See if the second arg is space or empty,
                    # if it is we'll try to use the third arg 
                    # and if that fails we'll then tell the user 
                    # that their syntax is wrong. 
                    if case_lines[1].isspace() or case_lines[1] == '':
                        try: command = case_lines[2]
                        except: raise SyntaxError(f"Default Case - The interpreter cannot find a case statement at line {line_number + 1}! Follow this format: `case statement:`")  
                    else: command = case_lines[1]

                    # If all that was sucessful we'll add the 
                    # command to the list to be executed soon!
                    self.command_list.append(command)

                else:
                    # If it isn't default or the users value
                    # we'll basically pass this case.
                    in_valid_case = False
            
            # Now we're on to the whole big brain stuff. We get 
            # to use all those bool variables! After all that 
            # we can add the users command to the command list
            # **if** we're in a valid case **and** in a valid 
            # case, if we aren't then we just continue or raise
            # a SyntaxError.
            else:

                if   not in_case:       raise SyntaxError(f"Syntax error at line {line_number + 1}!")
                elif not in_valid_case: continue 
                self.command_list.append(line)

#
#                                              Examples:
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

def ded():
    print("double ded")

case = """

switch (2):

case 1: 
    print("ok")

case 2:
    print("ded")

case "oh":
    ded()

case default:
    print("default case - catches everything else")

"""

value = 1
case2 = f"""

switch ({value}):

case 1:
    print("f strings work too!")

case default:
    print("E")

"""

# TODO: Test value in .case() 

switch1 = switch(clear_code=False)
switch1 . case(code=case)
switch1 . case(rerun=True)
# switch1 . case(code=case2, rerun=True)

#
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
