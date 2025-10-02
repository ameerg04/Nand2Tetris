"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from Parser import Parser
from CodeWriter import CodeWriter


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO, sys_write) -> None:
    """Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # Note: you can get the input file's name using:
    parsed = Parser(input_file)
    writer = CodeWriter(output_file)
    if sys_write:
        writer.writeInit()
    # iterate over the commands
    while parsed.has_more_commands():
        command = parsed.current
        # take every command, check its type, and write in the output-file accordingly
        c_type = parsed.command_type()
        if parsed.command_type() == "C_ARITHMETIC":
            writer.write_arithmetic(command)
        elif parsed.command_type() == "C_PUSH" or parsed.command_type() == "C_POP":
            command1 = command.split(" ")
            try:
                command2, segment, index = command1[0], command1[1], command1[2]
                # clearing the index from non numeric characters
                for i in range(len(index)):
                    if not index[i].isnumeric():
                        index = index[0:i]
                        break
                writer.write_push_pop(command2, segment, int(index),
                                      os.path.splitext(os.path.basename(input_file.name))[0])
            except:
                raise Exception("Command not valid")
        elif c_type == "C_LABEL":
            command1 = command.split(" ")
            writer.writeLabel(command1[1])
        elif c_type == "C_GOTO":
            command1 = command.split(" ")
            writer.writeGoTo(command1[1])
        elif c_type == "C_IF":
            command1 = command.split(" ")
            writer.writeIf(command1[1])
        elif c_type == "C_FUNCTION":
            writer.writeFunction(command)
        elif c_type == "C_RETURN":
            writer.writeReturn()
        elif c_type == "C_CALL":
            writer.writeCall(command)
        parsed.advance()
    # writing the last command
    command = parsed.current
    c_type1 = parsed.command_type()
    if parsed.command_type() == "C_ARITHMETIC":
        writer.write_arithmetic(command)
    elif parsed.command_type() == "C_PUSH" or parsed.command_type() == "C_POP":
        command1 = command.split(" ")
        try:
            command2, segment, index = command1[0], command1[1], command1[2]
            writer.write_push_pop(command2, segment, index, str(input_file))
        except:
            raise Exception("Command not valid")
    elif c_type1 == "C_LABEL":
        command1 = command.split(" ")
        writer.writeLabel(command1[1])

    elif c_type1 == "C_GOTO":
        command1 = command.split(" ")
        writer.writeGoTo(command1[1])
    elif c_type1 == "C_IF":
        command1 = command.split(" ")
        writer.writeIf(command1[1])
    elif c_type1 == "C_FUNCTION":
        writer.writeFunction(command)
    elif c_type1 == "C_RETURN":
        writer.writeReturn()
    elif c_type1 == "C_CALL":
        writer.writeCall(command)


if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file
    sys_check = False
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
        if "Sys.vm" in str(files_to_translate):  # check if we have sys in the directory
            sys_check = True
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, sys_check)
