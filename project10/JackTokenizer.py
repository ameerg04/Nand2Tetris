"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing


class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Your code goes here!
        # A good place to start is:
        self.input_lines = []
        self.commands_done = 0  # number of lines in the clean file
        self.token_counter = 0  # number of token in the line
        self.token = ""
        self.keyword = {'class', 'constructor', 'function', 'method', 'field'
            , 'static', 'var', 'int', 'char', 'boolean', 'void'
            , 'true', 'false', 'null', 'this', 'let', 'do',
                        'if', 'else', 'while', 'return'}
        self.symbols = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-'
            , '*', '/', '&', '|', '<', '>', '=', '~'}

        self.file_lines = input_stream.read().splitlines()
        self.clean_lst()
        self.counter = 0  # number of commands in the file
        for line in self.input_lines:
            self.counter += len(line)

    def clean_lst(self):
        """
        cleans the lines of the list from whitespaces and comments
        """
        for line in self.file_lines:
            line = line.strip()  # delete spaces
            first_comment = line.startswith("*")
            second_comment = line.startswith("/**")
            third_comment = line.startswith("*/")
            double_slash = line.find("//")
            if double_slash != 0 and line != "" and line != "\n":
                if not first_comment and not second_comment and not third_comment:
                    if double_slash != -1:
                        line = line[:double_slash]
                        line = line.strip()
                    self.input_lines.append(line)

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        # Your code goes here!
        return len(self.input_lines) != self.commands_done + 1

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token.
        This method should be called if has_more_tokens() is true.
        Initially there is no current token.
        """
        flag = 0
        if self.has_more_tokens():
            line = self.input_lines[self.commands_done]
            if self.token_counter == len(line):
                self.commands_done += 1
                self.token_counter = 0
            line = self.input_lines[self.commands_done]
            while line[self.token_counter] == " ":
                self.token_counter += 1
            if line[self.token_counter] in self.symbols:
                flag = 1
                self.token = line[self.token_counter]
                self.token = self.symbol()
                self.token_counter += 1
            elif line[self.token_counter] == '"':
                flag = 1
                self.token = ""
                self.token += '"'
                self.token_counter += 1
                while line[self.token_counter] != '"':
                    self.token += line[self.token_counter]
                    self.token_counter += 1
                self.token += '"'
                self.token_counter += 1
            elif line[self.token_counter].isnumeric():
                self.token = ""
                flag = 1
                while line[self.token_counter].isnumeric():
                    self.token += str(line[self.token_counter])
                    self.token_counter += 1
                self.token = int(self.token)
            elif line[self.token_counter].isalpha():
                token = ""
                counter = 0
                while line[self.token_counter].isalpha():
                    token += line[self.token_counter]
                    self.token_counter += 1
                    counter += 1
                if token in self.keyword:
                    flag = 1
                    self.token = token
                else:
                    flag = 0
                    self.token_counter -= counter
            if flag == 0:
                token = ""
                while (line[self.token_counter] != " " or line[self.token_counter] == "_") \
                        and line[self.token_counter] not in self.symbols:
                    token += line[self.token_counter]
                    self.token_counter += 1
                self.token = token

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        if self.token in self.symbols:
            return "SYMBOL"
        elif self.token in self.keyword:
            return "KEYWORD"
        elif type(self.token) == int:
            return "INT_CONST"
        elif self.token[0] == '"':
            return "STRING_CONST"
        else:
            return "IDENTIFIER"

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT",
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO",
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        # Your code goes here!
        if self.token_type() == "KEYWORD":
            return self.token

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
        """
        # Your code goes here!
        if self.token_type() == "SYMBOL":
            if self.token == "&":
                return "&amp"
            elif self.token == "<":
                return "&lt"
            elif self.token == ">":
                return "&gt"
            else:
                return self.token

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
        """
        # Your code goes here!
        pass

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
        """
        # Your code goes here!
        if self.token_type() == "INT_CONST":
            return int(self.token)

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double
            quotes. Should be called only when token_type() is "STRING_CONST".
        """
        # Your code goes here!\
        if self.token_type() == "STRING_CONT":
            return self.token

    def get_token(self):
        return self.token
