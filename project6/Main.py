"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from SymbolTable import SymbolTable
from Parser import Parser
from Code import Code


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    
    symbol_table = SymbolTable()
    parsed_file = Parser(input_file)
    # starting first pass
    parsed_file.advance()
    for num in range(len(parsed_file.input_lines)):
        if not parsed_file.is_command(num):
            continue
        curr_command = parsed_file.get_command()
        if parsed_file.command_type() == "L_COMMAND":
            symbol_table.add_entry(curr_command[1:-1], parsed_file.commands_so_far)
        else:
            parsed_file.commands_so_far += 1
        parsed_file.advance()
    # starting second pass
    index = 16
    parsed_file.current = parsed_file.input_lines[0]
    parsed_file.index = 0
    parsed_file.advance()
    # adding A instructions to the symbol table
    while parsed_file.has_more_commands():
        command = parsed_file.get_command()
        if parsed_file.command_type() == "A_COMMAND":
            symbol = parsed_file.symbol()
            if not symbol_table.contains(symbol) and not symbol.isnumeric():
                symbol_table.add_entry(symbol, index)
                index += 1
            elif not symbol_table.contains(symbol):
                # c = int(symbol)
                symbol_table.add_entry(command[1:], int(symbol))
        parsed_file.advance()
    # write the output file
    parsed_file.current = parsed_file.input_lines[0]
    parsed_file.index = 0
    parsed_file.advance()
    for i in range(len(parsed_file.input_lines)):
        if not parsed_file.is_command(i):
            continue
        command = parsed_file.get_command()
        if parsed_file.command_type() == "A_COMMAND":
            line = parsed_file.symbol()
            if line[0].isnumeric():
                binary = bin(int(line))
                binary = binary[:1] + binary[2:]
                binary = (16 - len(binary)) * "0" + binary
                output_file.write(binary + "\n")
            else:
                address = symbol_table.get_address(line)
                binary = bin(int(address))
                binary = binary[:1] + binary[2:]
                binary = (16 - len(binary)) * "0" + binary
                output_file.write(binary + "\n")
        if parsed_file.command_type() == "C_COMMAND":
            code = Code()
            output_file.write(code.translate_instruction(command) + "\n")
        parsed_file.advance()


if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
