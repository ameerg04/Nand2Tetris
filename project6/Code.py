"""This file is part of nand2tetris, as taught in The Hebrew University,
and was written by Aviv Yaish according to the specifications given in  
https://www.nand2tetris.org (Shimon Schocken and Noam Nisan, 2017)
and as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0 
Unported License (https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""


class Code:
    """Translates Hack assembly language mnemonics into binary codes."""

    @staticmethod
    def dest(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a dest mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        dest_vals = {"null": '000', 'M': '001', 'D': '010', 'MD': '011'
            , 'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}
        return dest_vals[mnemonic]

    @staticmethod
    def comp(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a comp mnemonic string.

        Returns:
            str: 7-bit long binary code of the given mnemonic.
        """
        comp_vals = {'0': '0101010', '1': '0111111', '-1': '0111010',
                     'D': '0001100',
                     'A': '0110000', '!D': '0001101', '!A': '0110001',
                     '-D': '0001111',
                     '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111',
                     'D-1': '0001110',
                     'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011',
                     'A-D': '0000111',
                     'D&A': '0000000', 'D|A': '0010101', 'M': '1110000',
                     '!M': '1110001',
                     '-M': '1110011', 'M+1': '1110111', 'M-1': '1110010',
                     'D+M': '1000010',
                     'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
                     'D|M': '1010101'}
        return comp_vals[mnemonic]

    @staticmethod
    def jump(mnemonic: str) -> str:
        """
        Args:
            mnemonic (str): a jump mnemonic string.

        Returns:
            str: 3-bit long binary code of the given mnemonic.
        """
        jump_vals = {"null": '000', 'JGT': '001', 'JEQ': '010', 'JGE': '011'
            , 'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}
        return jump_vals[mnemonic]

    def modify_instruction(self, instruction):
        """
        Take an instruction with white spaces and comments in the line
        of the instruction and return the text of the instruction alone
        :param instruction: The instruction line
        :return: The instruction text with no white spaces and comments
        """
        new_instruction = instruction.replace(" ", "")
        final_instruction = ""
        for i in range(len(new_instruction)):
            if new_instruction[i] != '/':
                final_instruction += new_instruction[i]
            else:
                break
        return final_instruction

    def translate_instruction(self, new_instruction):
        """
        We get an instruction and translate it intro it's binary form
        :param new_instruction: The c_instruction
        :return: Binary code of the instruction
        """
        # taking the text of the instruction
        new_instruction = self.modify_instruction(new_instruction)
        binary = "111"
        eq = new_instruction.find("=")
        mid = new_instruction.find(";")
        if ("=" in new_instruction) and (";" in new_instruction):
            return binary + self.comp(new_instruction[eq + 1:mid]) + \
                   self.dest(new_instruction[0:eq]) + self.jump(
                new_instruction[mid:-1])
        if ("=" in new_instruction) and (";" not in new_instruction):
            return binary + self.comp(new_instruction[eq + 1:len(new_instruction)]) + \
                   self.dest(new_instruction[0:eq]) + self.jump("null")
        if ("=" not in new_instruction) and (";" in new_instruction):
            return binary + self.comp(new_instruction[eq + 1:mid]) + \
                   self.dest("null") + self.jump(
                new_instruction[mid + 1:-1] + new_instruction[-1])
        if ("=" not in new_instruction) and (";" not in new_instruction):
            return binary + self.comp(new_instruction) + \
                   self.dest("null") + self.jump("null")
