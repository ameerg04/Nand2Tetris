"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the
    input code. It reads VM commands, parses them, and provides convenient 
    access to their components. 
    In addition, it removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Gets ready to parse the input file.

        Args:
            input_file (typing.TextIO): input file.
        """
        # Your code goes here!
        # A good place to start is:
        # input_lines = input_file.read().splitlines()
        self.input_lines = input_file.read().splitlines()
        # taking out all the white spaces in the lines
        self.commands_so_far = 0
        # what line we are at in the line
        self.index = self.update_index()
        # the current command we are at in the line
        self.current = self.input_lines[self.index]

    def update_index(self):
        for i in range(len(self.input_lines)):
            if self.input_lines[i] != "":
                if self.input_lines[i][0] != '/':
                    return i

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        # Your code goes here!
        if self.index >= len(self.input_lines):
            return False
        for i in range(self.index + 1, len(self.input_lines)):
            if self.input_lines[i] != "":
                if self.input_lines[i][0] != '/' and self.input_lines[i] != '\n':
                    return True
        return False

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current 
        command. Should be called only if has_more_commands() is true. Initially
        there is no current command.
        """
        # Your code goes here!
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
            str: the type of the current VM command.
            "C_ARITHMETIC" is returned for all arithmetic commands.
            For other commands, can return:
            "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
            "C_RETURN", "C_CALL".
        """
        arithmetic_operations = {'add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not', 'shiftleft', 'shiftright'}
        if self.current[:2] in arithmetic_operations:
            return "C_ARITHMETIC"
        if self.current[:3] in arithmetic_operations:
            return "C_ARITHMETIC"
        if self.current == 'shiftleft' or self.current == "shiftright":
            return "C_ARITHMETIC"
        command = self.current.split(" ")[0]
        if command == "pop":
            return "C_POP"
        if command == "push":
            return "C_PUSH"

    def arg1(self) -> str:
        """
        Returns:
            str: the first argument of the current command. In case of 
            "C_ARITHMETIC", the command itself (add, sub, etc.) is returned. 
            Should not be called if the current command is "C_RETURN".
        """
        if "pop" in self.current:
            return "pop"
        if "push" in self.current:
            return "push"
        if self.command_type() is "C_ARITHMETIC":
            return self.current

    def arg2(self) -> int:
        """
        Returns:
            int: the second argument of the current command. Should be
            called only if the current command is "C_PUSH", "C_POP", 
            "C_FUNCTION" or "C_CALL".
        """
        if "push" in self.current or "pop" in self.current:
            return self.current.split(" ")[2]
