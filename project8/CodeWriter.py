"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing


class CodeWriter:
    count = 0
    call_counter = 0
    init_counter = 0
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        self.eqi = 0
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
        if new_command == "or":
            asm = "@SP\nAM=M-1\nD=M\n@SP\nA=M-1\nM=D|M\n"
            self.output_file.write(asm)
            return
        if new_command == "eq":
            assemble_command = "@SP\nAM=M-1\nD=M\n@SP\nAM=M-1\nD=D-M\n@EQUAL_{f}\nD;JEQ\n@SP\n" \
                               "A=M\nM=0\n@END_{f}\n0;JMP\n(EQUAL_{f})\n@SP\nA=M\nM=-1\n(END_{f})\n@SP\nM=M+1\n".format(
                f=str(CodeWriter.count))
            CodeWriter.count += 1
            self.output_file.write(assemble_command)
            return
        if new_command == "lt":
            asm = "@32767\nD=!A\n@SP\nAM=M-1\nD=M&D\n@R14\nM=D\n@32767\nD=!A\n@SP\nA=M-1\n" \
                  "D=M&D\n@R13\nM=D\n@R14\nD=D-M\n@EQ_INDEX\nD;JEQ\n@R14\nD=M\n@TRUE_INDEX\n" \
                  "D;JEQ\n@SP\nA=M-1\nM=0\n@END_INDEX\n0;JMP\n(EQ_INDEX)\n@SP\nA=M\nD=M\n" \
                  "@SP\nAM=M-1\nD=M-D\nM=0\n@JMP_INDEX\nD;JGE\n@SP\nA=M\nM=-1\n(JMP_INDEX)\n" \
                  "@SP\nM=M+1\n@END_INDEX\n0;JMP\n(TRUE_INDEX)\n@SP\nA=M-1\nM=-1\n" \
                  "(END_INDEX)\n"
            final = asm.replace("INDEX", str(CodeWriter.count))
            CodeWriter.count += 1
            self.output_file.write(final)
            return

        elif new_command == "gt":
            asm = "@32767\nD=!A\n@SP\nAM=M-1\nD=M&D\n@R14\nM=D\n@32767\nD=!A\n@SP\nA=M-1\n" \
                  "D=M&D\n@R13\nM=D\n@R14\nD=D-M\n@EQ_INDEX\nD;JEQ\n@R13\nD=M\n@TRUE_INDEX\n" \
                  "D;JEQ\n@SP\nA=M-1\nM=0\n@END_INDEX\n0;JMP\n(EQ_INDEX)\n@SP\nA=M\nD=M\n@SP\n" \
                  "AM=M-1\nD=M-D\nM=0\n@JMP_INDEX\nD;JLE\n@SP\nA=M\nM=-1\n(JMP_INDEX)\n@SP\n" \
                  "M=M+1\n@END_INDEX\n0;JMP\n(TRUE_INDEX)\n@SP\nA=M-1\nM=-1\n" \
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

    def write_push_pop(self, command: str, segment: str, index: int, file_name: str) -> None:
        """Writes the assembly code that is the translation of the given
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        if segment == "static":
            if command == "push":
                # asm = "@" + str(index) + "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
                # self.output_file.write(asm)
                # return
                ind = str(index)
                asm = "@SP\nA=M-1\nD=M\n@file_name\nM=D\n@SP\nM=M-1\n"
                asm1 = asm.replace("file_name", str(file_name) + ind)
                self.output_file.write(asm1)
                return
            if command == "pop":
                ind = str(index)
                asm = "@SP\nA=M-1\nD=M\n@file_name\nM=D\n@SP\nM=M-1\n"
                asm1 = asm.replace("file_name", str(file_name) + ind)
                self.output_file.write(asm1)
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

    def writeLabel(self, string: str) -> None:
        """
        Writing the label command
        Args:
            string: The command we want to write

        Returns:

        """
        self.output_file.write("(" + string + ")\n")

    def writeGoTo(self, string: str) -> None:
        """
        writes goto commands

        Args:
            string:

        Returns:

        """
        asm = "@" + string + "\n0;JMP\n"
        self.output_file.write(asm)

    def writeIf(self, string: str) -> None:
        """

        Args:
            string:

        Returns:

        """
        asm = "@SP\nAM=M-1\nD=M\n@" + string + "\nD;JNE\n"
        self.output_file.write(asm)

    def writeFunction(self, string: str) -> None:
        """
        write the function command
        Args:
            string:

        Returns:
        """

        number = int(string.split()[2])
        function_name = string.split()[1]
        # write the function label
        self.writeLabel(function_name)
        for i in range(number):
            asm = "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
            self.output_file.write(asm)

    def writeReturn(self) -> None:
        asm = "@LCL\nD=M\n@endFrame\nM=D\n@5\nA=D-A\nD=M\n@retAddr\nM=D\n@SP\nA=M-1\nD=M\n@SP\nM=M-1\n@ARG\nA=M\nM=D\n" \
              "@ARG\nD=M+1\n@SP\nM=D\n@endFrame\nD=M\n@1\nA=D-A\nD=M\n@THAT\nM=D\n@endFrame\nD=M\n@2\nA=D-A\nD=M\n" \
              "@THIS\nM=D\n@endFrame\nD=M\n@3\nA=D-A\nD=M\n@ARG\nM=D\n@endFrame\nD=M\n@4\nA=D-A\nD=M\n@LCL\nM=D\n" \
              "@retAddr\nA=M\n0;JMP\n"
        self.output_file.write(asm)

    def writeCall(self, command: str):
        asm = "@1_{f}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" \
              "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" \
              "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@SP\nD=M\n@{x}\nD=D-A\n@5\nD=D-A\n" \
              "@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@{z}\n0;JMP\n(1_{f})\n".format(f=CodeWriter.call_counter,
                                                                              x=command.split()[2],
                                                                              z=command.split()[1])
        CodeWriter.call_counter += 1
        self.output_file.write(asm)

    def writeInit(self):
        """
        Writing the init
        Returns:
        """
        if CodeWriter.init_counter == 0:
            CodeWriter.init_counter += 1
            command_str = "@256\nD=A\n@SP\nM=D\n"
            self.output_file.write(command_str)
            self.writeCall("call Sys.init 0")


def close(self) -> None:
    """Closes the output file."""
    # Your code goes here!
    self.output_file.close()
