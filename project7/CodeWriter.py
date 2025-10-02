"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing
import Parser


class CodeWriter:
    count = 0
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.output_file = output_stream
        self.segments = {"argument", "local", "constant", "static", "this",
                         "that", "pointer", "temp"}

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is
        started.

        Args:
            filename (str): The name of the VM file.
        """
        pass

    def check_arithmentic(self, command: str):
        """
        In this function we take a command and check if we have an arithmetic command
        Args:
            command: The command we want to check

        Returns: The command we have, Raises an exception if the command is not arithmetic

        """
        arithmetic = {"add", "sub", "and", "neg", "not", "eq", "lt", "gt",
                      "or", "sheftleft", "sheftright"}

        for com in arithmetic:
            if com in command:
                return com
        raise Exception("command not valid")

    def write_arithmetic(self, command: str) -> None:
        """Writes the assembly code that is the translation of the given
        arithmetic command.

        Args:
            command (str): an arithmetic command.
        """
        new_command = self.check_arithmentic(command)
        if new_command == "add":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D+M\n"
            self.output_file.write(asm)
            return
        if new_command == "sub":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=M-D\n"
            self.output_file.write(asm)
            return
        if new_command == "neg":
            asm = "@SP\nA=M-1\nM=!M\nM=M+1\n"
            self.output_file.write(asm)
            return
        if new_command == "and":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D&M\n"
            self.output_file.write(asm)
            return
        if new_command == "not":
            asm = "@SP\nA=M-1\nM=!M\n"
            self.output_file.write(asm)
            return
        if new_command == "and":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D|M\n"
            self.output_file.write(asm)
            return
        if new_command == "eq":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=D-M\n@TRUE\nD;JEQ\n@SP\n" \
                  "A=M\nM=0\n@UPDATE\n0;JMP\n(TRUE)\n@SP\nA=M\nM=1\n(UPDATE)\n@SP\n" \
                  "M=M+1\n"
            self.output_file.write(asm)
            return
        if new_command == "lt":
            asm = "@32767\nD=!A\n@SP\nAM=M-1\nD=M&D\n@R11\nM=D\n@32767\nD=!A\n@SP\nA=M-1\n" \
                  "D=M&D\n@R10\nM=D\n@R13\nD=D-M\n@EQ_INDEX\nD;JEQ\n@R11\nD=M\n@TRUE_INDEX\n" \
                  "D;JEQ\n@SP\nA=M-1\nM=0\n@END_INDEX\n0;JMP\n(EQ_INDEX)\n@SP\nA=M\nD=M\n" \
                  "@SP\nAM=M-1\nD=M-D\nM=0\n@JMP_INDEX\nD;JGE\n@SP\nA=M\nM=-1\n(JMP_INDEX)\n" \
                  "@SP\nM=M+1\n@END_INDEX\n0;JMP\n(TRUE_INDEX)\n@SP\nA=M-1\nM=-1\n@END_INDEX\n0;JMP\n" \
                  "(END_INDEX)\n"
            final = asm.replace("INDEX", str(CodeWriter.count))
            CodeWriter.count += 1
            self.output_file.write(final)
            return

        if new_command == "gt":
            asm = "@32767\nD=!A\n@SP\nAM=M-1\nD=M&D\n@R11\nM=D\n@32767\nD=!A\n@SP\nA=M-1\n" \
                  "D=M&D\n@R10\nM=D\n@R13\nD=D-M\n@EQ_INDEX\nD;JEQ\n@R10\nD=M\n@TRUE_INDEX\n" \
                  "D;JEQ\n@SP\nA=M-1\nM=0\n@END_INDEX\n0;JMP\n(EQ_INDEX)\n@SP\nA=M\nD=M\n@SP\n" \
                  "AM=M-1\nD=M-D\nM=0\n@JMP_INDEX\nD;JLE\n@SP\nA=M\nM=-1\n(JMP_INDEX)\n@SP\n" \
                  "M=M+1\n@END_INDEX\n0;JMP\n(TRUE_INDEX)\n@SP\nA=M-1\nM=-1\n@END_INDEX\n0;JMP\n" \
                  "(END_INDEX)\n"
            final = asm.replace("INDEX", str(CodeWriter.count))
            CodeWriter.count += 1
            self.output_file.write(final)
            return

        if new_command == "sheftleft":
            asm = "@SP\nA=M-1\nM=M+1\n"
            self.output_file.write(asm)
            return
        if new_command == "shiftright":
            asm = "@SP\nA=M-1\nM=M-1\n"
            self.output_file.write(asm)
            return

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if segment == "static":
            if command == "push":
                asm = "@" + str(index) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                self.output_file.write(asm)
                return
            if command == "pop":
                asm = "@SP\nA=M-1\nD=M\n@" + str(index) + "\nM=D\n@SP\nM=M-1\n"
                self.output_file.write(asm)
                return
        if segment == "temp":
            if command == "push":
                asm = "@" + str(index) + "\nD=A\n@5\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                self.output_file.write(asm)
                return
            if command == "pop":
                asm = "@" + str(index) + "\nD=A\n@5\nD=D+A\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n"
                self.output_file.write(asm)
                return
        if segment == "pointer":
            # index check
            if index != 0 and index != 1:
                raise Exception("Index not valid")
            if index == 0 and command == "push":  # This and push
                asm = "@THIS\nD=M\n@" + str(index) + "\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                self.output_file.write(asm)
                return
            if index == 0 and command == "pop":  # This and pop
                asm = "@THIS\nD=A\n@" + str(
                    index) + "\nD=D+A\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n"
                self.output_file.write(asm)
                return
            if index == 1 and command == "push":  # That and push
                asm = "@THAT\nD=M\n@" + str(index) + "\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                self.output_file.write(asm)
                return
            if index == 1 and command == "pop":  # That and pop
                asm = "@THAT\nD=A\n@" + str(
                    index) + "\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n"
                self.output_file.write(asm)
                return
        if segment == "constant":
            if command == "push":
                asm = "@" + str(index) + "\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                self.output_file.write(asm)
                return
            if command == "pop":
                asm = "@SP\nA=M-1\nD=M\n@" + str(index) + "\nM=D\n@SP\nM=M-1\n"
                self.output_file.write(asm)
                return
        else:  # dealing with local and arguments and this and that
            push_command = "@SEG\nD=M\n@" + str(index) + "\nA=A+D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
            pop_command = "@SEG\nD=M\n@" + str(
                index) + "\nD=D+A\n@R13\nM=D\n@SP\nA=M-1\nD=M\n@R13\nA=M\nM=D\n@SP\nM=M-1\n"
            if command == "push":
                if segment == "local":
                    self.output_file.write(push_command.replace("SEG", "LCL"))
                    return
                if segment == "argument":
                    self.output_file.write(push_command.replace("SEG", "ARG"))
                    return
                if segment == "this":
                    self.output_file.write(push_command.replace("SEG", "THIS"))
                    return
                if segment == "that":
                    self.output_file.write(push_command.replace("SEG", "THAT"))
            if command == "pop":
                if segment == "local":
                    self.output_file.write(pop_command.replace("SEG", "LCL"))
                    return
                if segment == "argument":
                    self.output_file.write(pop_command.replace("SEG", "ARG"))
                    return
                if segment == "this":
                    self.output_file.write(pop_command.replace("SEG", "THIS"))
                    return
                if segment == "that":
                    self.output_file.write(pop_command.replace("SEG", "THAT"))

    def close(self) -> None:
        """Closes the output file."""
        # Your code goes here!
        self.output_file.close()
