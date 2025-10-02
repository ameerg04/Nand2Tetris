"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """Encapsulates access to the input code. Reads and assembly language 
    command, parses it, and provides convenient access to the commands 
    components (fields and symbols). In addition, removes all white space and 
    comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        self.input_lines = input_file.read().splitlines()
        # taking out all the white spaces in the lines
        for i in range(len(self.input_lines)):
            self.input_lines[i].replace(" ", "")
        self.commands_so_far = 0
        # what line we are at in the line
        self.index = 0
        # the current command we are at in the line
        self.current = self.input_lines[0]

    def get_command(self):
        return self.current

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        if self.index >= len(self.input_lines):
            return False
        for i in range(self.index + 1, len(self.input_lines)):
            if self.input_lines[i] != "":
                if self.input_lines[i][0] != '/' and self.input_lines[i] != '\n':
                    return True
        return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        if self.has_more_commands():
            for i in range(self.index + 1, len(self.input_lines)):
                if self.input_lines[i] != "":
                    if self.input_lines[i][0] != '/' and self.input_lines[i] != " " and self.input_lines[i] != "":
                        self.index = i
                        self.current = self.input_lines[self.index]
                        break

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        if "@" in self.current:
            return "A_COMMAND"
        elif "(" in self.current[0]:
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        output = ""
        if self.command_type() == "L_COMMAND":
            brackets = self.current.find(")")
            for i in range(brackets):
                if self.current[i] == " " or self.current[i] == "(":
                    continue
                output += self.current[i]
        if self.command_type() == "A_COMMAND":
            for i in range(len(self.current)):
                if self.current[i] == "@":
                    for j in range(i + 1, len(self.current)):
                        if self.current[j] != "" and self.current[j] != '/' and self.current[j] != " ":
                            output += self.current[j]
                        else:
                            break
            return output
        return ""

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.command_type() == "C_COMMAND":
            equal = self.current.find("=")
            if equal == -1:
                return ""
            return self.current[0:equal]

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.dest() == "":
            eq = self.current.find(";")
            return self.current[0:eq]
        d = len(self.dest()) + 2
        return self.current[d:-1]

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        if self.dest() == "":
            eq = self.current.find(";")
            return self.current[eq:-1]
        return ""

    def is_command(self, index):
        """
        In this function we get an index indicating the line we are at in the file
        and check if we have a command in this line
        :param index: number indicating the line we are at in the file
        :return: True if we have a command in this line, False otherwise
        """
        if self.input_lines[index] == "":
            return False
        if self.input_lines[index] != "":
            if self.input_lines[index][0] == '/':
                return False
        return True
