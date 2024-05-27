from math import log2

from Encoder import Encoder


class SimpleEncoder(Encoder):
    def __init__(self, block_size: int):
        super().__init__(block_size)
        if not log2(block_size).is_integer():
            raise ValueError("block size must be a power of 2")
        self.block_size = block_size

    def encode(self, data: str, block: list[int], verbose: bool = False):
        if verbose:
            print("Using Simple Encoder")

        max_data_length = self.block_size

        if len(data) > max_data_length:
            raise ValueError("Data is too long")

        while len(data) < max_data_length:
            data += '0'

        data_reversed = list(map(int, data[::-1]))

        for index, _ in enumerate(block):
            block[index] = data_reversed.pop()

        if verbose:
            print(f'encoded data: {block}')

    def decode(self, block: list[int], fix_inplace: bool = False, verbose: bool = False) -> str:
        self.validate(block, fix_inplace, verbose)

        result = ''.join(map(str, block))

        if verbose:
            print(f'decoded data: {result}')

        return result

    @staticmethod
    def validate(block: list[int], inplace: bool = False, verbose: bool = False) -> bool:
        if verbose:
            print('No Errors detected')
        return True
