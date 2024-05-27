from math import log2
from functools import reduce
from operator import xor
from Encoder import Encoder


class HammingEncoder(Encoder):
    def __init__(self, block_size: int):
        super().__init__(block_size)
        if not log2(block_size).is_integer():
            raise ValueError("block size must be a power of 2")
        self.max_data_size = self.block_size - 1 - int(log2(self.block_size))

    def encode(self, data: str, block: list[int], verbose: bool = False):
        if verbose:
            print("Using Hamming Encoder")

        if len(data) > self.max_data_size:
            raise ValueError("Data is too long")

        while len(data) < self.max_data_size:
            data += '0'

        data_reversed = list(map(int, data[::-1]))

        for index, _ in enumerate(block):
            if index == 0 or log2(index).is_integer():
                continue

            block[index] = data_reversed.pop()

        self._fill_redundancy_bits_hamming(block)

        if verbose:
            print(f'encoded data: {block}')

    def decode(self, block: list[int], fix_inplace: bool = False, verbose: bool = False) -> str:
        self.validate(block, fix_inplace, verbose)

        result = ''

        for index, message_bit in enumerate(block):
            if index == 0 or log2(index).is_integer():
                continue
            result += str(message_bit)

        if verbose:
            print(f'decoded data: {result}')

        return result

    @staticmethod
    def validate(block: list[int], inplace: bool = False, verbose: bool = False) -> bool:
        error_position = reduce(xor, [i for i, bit in enumerate(block) if bit], 0)
        if error_position == 0:
            if verbose:
                print('No Errors detected')
            return True

        if inplace:
            block[error_position] = 1 - block[error_position]

        if verbose:
            if inplace:
                print('Fixing: ', end='')
            print(f'Error at index {error_position}')

        return False

    def _fill_redundancy_bits_hamming(self, block: list[int]):
        number_of_checks = int(log2(self.block_size))

        for i in range(number_of_checks):
            ones_count = 0
            for index, message_bit in enumerate(block):
                bin_index = format(index, f'0{int(log2(self.block_size))}b')
                if bin_index[-i - 1] == '1':
                    if message_bit == 1:
                        ones_count += 1
            block[2 ** i] = ones_count % 2

        total_ones_count = 0
        for message_bit in block:
            if message_bit == 1:
                total_ones_count += 1

        block[0] = total_ones_count % 2
