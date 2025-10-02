"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from JackTokenizer import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: typing.TextIO,
                 output_stream: typing.TextIO, tokenizer: JackTokenizer) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        :param tokenizer: A JackTokenizer object that works in our input stream
        """
        # Your code goes here!
        self.output_file = output_stream
        self.input = input_stream
        self.tokenizer = tokenizer
        self.constant_terms_set = {"false", "true", "this", "null"}
        self.operations_set = {"+", "-", "=", "&lt", "&gt", "&amp", "|", "*", "/"}
        self.statement_set = {"else", "if", "while", "do", "return", "let"}

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.output_file.write("<class>\n")
        self.tokenizer.advance()
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.token == "{":
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
            elif self.tokenizer.token_type() == "SYMBOL":
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
            elif self.tokenizer.token_type() == "STRING_CONST":
                self.output_file.write("<stringConstant> " + self.tokenizer.token + " </stringConstant>\n")
            elif self.tokenizer.token_type() == "INT_CONST":
                self.output_file.write("<integerConstant> " + str(self.tokenizer.token) + " </integerConstant>\n")
            elif self.tokenizer.token in self.statement_set:
                self.compile_statements()
            elif self.tokenizer.token == "static" or self.tokenizer.token == "field":
                self.compile_class_var_dec()
            elif self.tokenizer.token == "method" or self.tokenizer.token == "function" or self.tokenizer.token == "constructor":
                self.compile_subroutine()
            elif self.tokenizer.token_type() == "KEYWORD":
                self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")
            elif self.tokenizer.token_type() == "IDENTIFIER":
                self.output_file.write("<identifier> " + self.tokenizer.token + " </identifier>\n")
            self.tokenizer.advance()
        self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
        self.output_file.write("</class>\n")

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.output_file.write("<classVarDec>\n<keyword> " + self.tokenizer.token + " </keyword>\n")
        self.tokenizer.advance()
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.token_type() == "KEYWORD":
                self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")
            elif self.tokenizer.token_type() == "IDENTIFIER":
                self.output_file.write("<identifier> " + self.tokenizer.token + " </identifier>\n")
            elif self.tokenizer.token == ",":
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
            elif self.tokenizer.token == ";":
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
                break
            self.tokenizer.advance()
        self.output_file.write("</classVarDec>\n")

    def compile_subroutine(self) -> None:
        """Compiles a complete method, function, or constructor."""
        # Your code goes here!
        counter = 0
        self.output_file.write("<subroutineDec>\n<keyword> " + self.tokenizer.token + " </keyword>\n")
        self.tokenizer.advance()
        while self.tokenizer.has_more_tokens():
            if counter == 0:  # void|type
                if self.tokenizer.token_type() == "KEYWORD":
                    self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")
                else:
                    self.output_file.write("<identifier> " + self.tokenizer.token + " </identifier>\n")
            elif counter == 1:  # subroutine name
                self.output_file.write("<identifier> " + self.tokenizer.token + "</identifier>\n")
            elif counter == 2:  # write the subroutine list -> (list)
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")  # write (
                self.tokenizer.advance()  # get to the parameters list
                self.compile_parameter_list()
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")  # write )
            elif counter == 3:  # write subroutine body -> write { body
                # start writing the body
                self.output_file.write("<subroutineBody>\n")
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")  # write to {
                while self.tokenizer.has_more_tokens():
                    # writing var statements if we have any
                    self.tokenizer.advance()
                    if self.tokenizer.token == "var":
                        self.compile_var_dec()
                    else:
                        break
                # once we are done with var declarations we check if we have statements to write or not
                if self.tokenizer.token == "}":  # the subroutine body is finished
                    self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
                    self.output_file.write("</subroutineBody>\n")
                    break
                else:  # we have statements in the subroutine
                    self.compile_statements()
                    self.tokenizer.advance()
                    self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")  # write }
                    self.output_file.write("</subroutineBody>\n")
                    break
            else:  # we finished writing the subroutine
                break
            counter += 1
            self.tokenizer.advance()
        self.output_file.write("</subroutineDec>\n")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the
        enclosing "()".
        """
        # Your code goes here!
        self.output_file.write("<parameterList>\n")
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.token_type() == "KEYWORD":  # writing keyword (type)
                self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")
            elif self.tokenizer.token == ",":  # in case we have more than one parameter
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
            elif self.tokenizer.token == ")":  # reached the end of list
                break
            else:  # write the name of the parameter
                self.output_file.write("<identifier> " + self.tokenizer.token + " </identifier>\n")
            self.tokenizer.advance()
        self.output_file.write("</parameterList>\n")

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        self.output_file.write("<varDec>\n")
        self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")  # writing var
        self.tokenizer.advance()
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.token_type() == "KEYWORD":  # writing the type
                self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")  # writing the type
            elif self.tokenizer.token_type() == "IDENTIFIER":  # writing the name of the var
                self.output_file.write("<identifier> " + self.tokenizer.token + " </identifier>\n")
            elif self.tokenizer.token == ',':  # writing ,
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")  # writing the ,
            else:  # we got to ;
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")  # writing the ;
                break
            self.tokenizer.advance()
        self.output_file.write("</varDec>\n")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing
        "{}".
        """
        # Your code goes here!
        self.output_file.write("<statements>\n")
        if self.tokenizer.token == "while":
            self.compile_while()
        elif self.tokenizer.token == "if":
            self.compile_if()
        elif self.tokenizer.token == "let":
            self.compile_let()
        elif self.tokenizer.token == "do":
            self.compile_do()
        elif self.tokenizer.token == "return":
            self.compile_return()
        while self.tokenizer.token in self.statement_set:
            if self.tokenizer.token == "while":
                self.compile_while()
            elif self.tokenizer.token == "if":
                self.compile_if()
            elif self.tokenizer.token == "let":
                self.compile_let()
            elif self.tokenizer.token == "do":
                self.compile_do()
            elif self.tokenizer.token == "return":
                self.compile_return()
        self.output_file.write("</statements>\n")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.output_file.write("<doStatement>\n")
        self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")
        token_counter = 0
        before = ""
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            after = self.tokenizer.token
            if token_counter == 0:
                before = self.tokenizer.token
            elif token_counter == 1:
                self.output_file.write("<identifier> " + before + " </identifier>\n")
                self.output_file.write("<symbol> " + after + " <symbol>\n")
                counter = 0
                flag = False
                while self.tokenizer.has_more_tokens():
                    if self.tokenizer.token == "." and counter == 0:
                        flag = True
                    self.tokenizer.advance()
                    if flag is True and counter == 0:
                        self.output_file.write("<identifier> ")
                        self.output_file.write(self.tokenizer.token)
                        self.output_file.write("</identifier>\n")
                    elif flag is True and counter == 1:
                        self.output_file.write("<symbol>")
                        self.output_file.write(self.tokenizer.token)
                        self.output_file.write("</symbol>\n")
                    elif (flag is True and counter == 2) or counter == 0:
                        self.compile_expression_list()
                        self.output_file.write("<symbol>")
                        self.output_file.write(self.tokenizer.token)
                        self.output_file.write("</symbol>\n")
                    else:
                        break
                    counter += 1
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.token)
                self.output_file.write("</symbol>\n")
            else:
                break
            token_counter += 1
        self.output_file.write("</doStatement>\n")

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self.output_file.write("<letStatement>\n")
        self.output_file.write("<keyword>")
        self.output_file.write(self.tokenizer.get_token())
        self.output_file.write("</keyword>\n")
        count, token_counter = 0, 0
        flag = False
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if flag:
                if token_counter == 0:
                    self.compile_expression()
                    self.output_file.write("<symbol>")
                    self.output_file.write(self.tokenizer.get_token())
                    self.output_file.write("</symbol>\n")
                elif token_counter == 1:
                    flag = False
                    count += 1
                    self.output_file.write("<symbol>")
                    self.output_file.write(self.tokenizer.get_token())
                    self.output_file.write("</symbol>\n")
                token_counter += 1
                continue
            if count == 0:
                self.output_file.write("<identifier>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</identifier>\n")
            elif count == 1:
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</symbol>\n")
                if self.tokenizer.get_token() != '=':
                    if self.tokenizer.has_more_tokens():
                        flag = True
                        continue
            elif count == 2:
                self.compile_expression()
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</symbol>\n")
            else:
                break
            count += 1

        self.output_file.write("</letStatement>\n")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.output_file.write("<whileStatement>\n")
        self.output_file.write("<keyword> " + self.tokenizer.get_token() + " </keyword>\n")
        token_counter = 0
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if token_counter == 0:  # writing (
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
            elif token_counter == 1:  # writing expression)
                self.compile_expression()
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")

            elif token_counter == 2:  # writing {
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
            elif token_counter == 3:  # writing statements }
                self.compile_statements()
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
                self.tokenizer.advance()
                break
            token_counter += 1
        self.output_file.write("</whileStatement>\n")

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.output_file.write("<returnStatement>\n")
        self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.token != ";":
                self.compile_expression()
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
            else:
                self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
        self.output_file.write("</returnStatement>\n")

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!

        self.output_file.write("<ifStatement>\n")
        self.output_file.write("<keyword> " + self.tokenizer.get_token() + " </keyword>\n")
        token_counter = 0
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.get_token() == "}":
                break
            self.tokenizer.advance()
            if token_counter == 0:  # write (
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</symbol>\n")
            elif token_counter == 1:  # write expression)
                self.compile_expression()
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</symbol>\n")
            elif token_counter == 2:  # write {
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</symbol>\n")
            elif token_counter == 3:  # write the statements in if and }
                self.compile_statements()
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</symbol>\n")
            elif token_counter == 4:
                break
            token_counter += 1
        if self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.get_token() == "else":
                self.output_file.write("<keyword> " + self.tokenizer.token + " </keyword>\n")
                counter = 0
                while self.tokenizer.has_more_tokens():
                    self.tokenizer.advance()
                    if counter == 0:  # write {
                        self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")

                    elif counter == 1:  # write statements in else and }
                        self.compile_statements()
                        self.output_file.write("<symbol> " + self.tokenizer.token + " </symbol>\n")
                    elif token_counter == 2:
                        break
                    counter += 1
            self.output_file.write("</ifStatement>\n")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.output_file.write("<expression>\n")
        self.compile_term()
        while self.tokenizer.has_more_tokens() and self.tokenizer.token in self.operations_set:

            self.output_file.write("<symbol>")
            if self.tokenizer.token == "&amp" or self.tokenizer.token == "&lt" or self.tokenizer.token == "&gt":
                self.output_file.write(self.tokenizer.token + ";" + "</symbol>\n")
            else:
                self.output_file.write(self.tokenizer.token + "</symbol>\n")
            self.tokenizer.advance()
            self.compile_term()
        self.output_file.write("</expression>\n")

    def term_write_in_file(self, command, token):
        """
        takes a command and a token and writes them in xml format in the output file
        """
        self.output_file.write("<" + command + ">" + token + "</" + command + ">\n")

    def compile_term(self) -> None:
        """Compiles a term.
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here
        self.output_file.write("<term>\n")
        flag = None
        current_token = self.tokenizer.token
        if self.tokenizer.token in self.constant_terms_set:
            self.term_write_in_file("keyword", self.tokenizer.token)
        elif self.tokenizer.token_type() == "STRING_CONST":
            self.term_write_in_file("stringConstant", self.tokenizer.token[1:-1])
        elif self.tokenizer.token_type() == "INT_CONST":
            self.term_write_in_file("integerConstant", str(self.tokenizer.token))
        elif self.tokenizer.token == "-":
            self.term_write_in_file("symbol", self.tokenizer.token)
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
                self.compile_term()
                flag = False
        elif self.tokenizer.token == "~":
            self.term_write_in_file("symbol", self.tokenizer.token)
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
                self.compile_term()
                flag = False
        elif self.tokenizer.token == "(":
            self.term_write_in_file("symbol", self.tokenizer.token)
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
                current_token = self.tokenizer.token
                self.compile_expression()
                self.term_write_in_file("symbol", str(self.tokenizer.token))
        else:
            flag = True
        if flag is None and self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            flag = False
        if flag is True:
            before = self.tokenizer.token
            before_type = self.tokenizer.token_type()
            if self.tokenizer.has_more_tokens():
                self.tokenizer.advance()
                after = self.tokenizer.token
                if after != '(' and after != "." and after != '[':
                    if before_type == "IDENTIFIER":
                        self.term_write_in_file("identifier", before)
                    elif before_type == "KEYWORD":
                        self.term_write_in_file("keyword", before)

                elif after == '.' or after == '(':
                    self.term_write_in_file("identifier", before)
                    self.term_write_in_file("symbol", self.tokenizer.token)
                    counter = 0
                    flag_2 = False
                    while self.tokenizer.has_more_tokens():
                        if self.tokenizer.token == "." and counter == 0:
                            flag_2 = True
                        self.tokenizer.advance()
                        if flag_2 is True and counter == 0:
                            self.term_write_in_file("identifier", self.tokenizer.token)
                        elif flag_2 is True and counter == 1:
                            self.term_write_in_file("symbol", self.tokenizer.token)
                        elif (flag_2 is True and counter == 2) or counter == 0:
                            self.compile_expression_list()
                            self.term_write_in_file("symbol", self.tokenizer.token)
                        else:
                            break
                        counter += 1
                elif after == "[":
                    self.term_write_in_file("identifier", before)
                    self.term_write_in_file("symbol", after)
                    if self.tokenizer.has_more_tokens():
                        self.tokenizer.advance()
                        self.compile_expression()
                        self.term_write_in_file("symbol", self.tokenizer.token)
                        if self.tokenizer.has_more_tokens():
                            self.tokenizer.advance()
        self.output_file.write("</term>\n")

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.output_file.write("<expressionList>\n")
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.get_token() == ",":
                self.output_file.write("<symbol>")
                self.output_file.write(self.tokenizer.get_token())
                self.output_file.write("</symbol>\n")
                if self.tokenizer.has_more_tokens():
                    self.tokenizer.advance()
            elif self.tokenizer.get_token() == ")":
                break
            else:
                self.compile_expression()
        self.output_file.write("</expressionList>\n")
