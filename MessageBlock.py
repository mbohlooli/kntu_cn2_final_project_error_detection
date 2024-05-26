from abc import ABC, abstractmethod
from functools import reduce
from operator import xor
from math import log2

HAMMING_ENCODE = "hamming"
PARITY_2D_ENCODE = "parity_2d"


class MessageBlock(ABC):
    def __init__(self, encoding):
        self.encoding = encoding

    @abstractmethod
    def write(self, data: str, verbose: bool = False) -> None:
        pass

    @abstractmethod
    def read(self, verbose: bool = False) -> str:
        pass

    @abstractmethod
    def validate(self, verbose: bool = False) -> None:
        pass


class ArrayMessageBlock(MessageBlock):
    def __init__(self, encoding=HAMMING_ENCODE, data='', block_size=16):
        super().__init__(encoding)
        self.block_size = block_size
        self.message = [0 for _ in range(block_size)]

        if len(data) > 0:
            self.write(data)

    def write(self, data: str, verbose: bool = False) -> None:
        if self.encoding == HAMMING_ENCODE:
            self._write_hamming(data, verbose)

    def read(self, verbose: bool = False) -> str:
        if self.encoding == HAMMING_ENCODE:
            return self._read_hamming(verbose)

    def validate(self, verbose: bool = False, inplace: bool = False) -> bool:
        if self.encoding == HAMMING_ENCODE:
            return self._validate_message_hamming(verbose, inplace)
        return False

    def __str__(self):
        return ''.join(map(str, self.message))

    def _read_hamming(self, verbose: bool = False) -> str:
        self.validate(verbose)

        result = ''

        for index, message_bit in enumerate(self.message):
            if index == 0 or log2(index).is_integer():
                continue
            result += str(message_bit)

        if verbose:
            print(f'decoded data: {result}')

        return result

    def _write_hamming(self, data: str, verbose: bool = False) -> None:
        max_data_length = self.block_size - 1 - int(log2(self.block_size))

        if len(data) > max_data_length:
            raise ValueError("Data is too long")

        while len(data) < max_data_length:
            data += '0'

        data_reversed = list(map(int, data[::-1]))

        for index, _ in enumerate(self.message):
            if index == 0 or log2(index).is_integer():
                continue

            self.message[index] = data_reversed.pop()

        self._fill_redundancy_bits_hamming()

        if verbose:
            print(f'encoded data: {self.message}')

    def _fill_redundancy_bits_hamming(self):
        number_of_checks = int(log2(self.block_size))

        for i in range(number_of_checks):
            ones_count = 0
            for index, message_bit in enumerate(self.message):
                bin_index = format(index, f'0{int(log2(self.block_size))}b')
                if bin_index[-i-1] == '1':
                    if message_bit == 1:
                        ones_count += 1
            self.message[2**i] = ones_count % 2

        total_ones_count = 0
        for message_bit in self.message:
            if message_bit == 1:
                total_ones_count += 1

        self.message[0] = total_ones_count % 2

    def _validate_message_hamming(self, verbose: bool = False, inplace: bool = False):
        error_position = reduce(xor, [i for i, bit in enumerate(self.message) if bit], 0)
        if error_position == 0:
            if verbose:
                print('No Errors detected')
            return True

        if inplace:
            self.message[error_position] = 1 - self.message[error_position]

        if verbose:
            print(f'Error at index {error_position}')

        return False

# TODO: do we really need this?
class MatrixMessageBlock(MessageBlock):
    def write(self, data: str, verbose: bool = False) -> None:
        pass

    def read(self, verbose: bool = False) -> str:
        pass

    def validate(self, verbose: bool = False) -> None:
        pass
