from abc import ABC, abstractmethod
from math import log2

HAMMING_ENCODE = "hamming"
PARITY_2D_ENCODE = "parity_2d"


class MessageBlock(ABC):
    @property
    @abstractmethod
    def encoding(self) -> str:
        pass

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
    def __init__(self):
        self.message = [0 for _ in range(16)]

    def write(self, data: str, verbose: bool = False) -> None:
        if len(data) > 11:
            raise ValueError("Data is too long")

        while len(data) < 11:
            data += '0'

        data_reversed = list(map(int, data[::-1]))

        for index, _ in enumerate(self.message):
            if index == 0 or log2(index).is_integer():
                continue

            self.message[index] = data_reversed.pop()

        if verbose:
            print(f'encoded data: {self.message}')

    def read(self, verbose: bool = False) -> str:
        result = ''

        for index, message_bit in enumerate(self.message):
            if index == 0 or log2(index).is_integer():
                continue
            result += str(message_bit)

        if verbose:
            print(f'decoded data: {result}')

        return result

    def validate(self, verbose: bool = False) -> None:
        pass

    def encoding(self) -> str:
        return HAMMING_ENCODE


class MatrixMessageBlock(MessageBlock):
    def write(self, data: str, verbose: bool = False) -> None:
        pass

    def read(self, verbose: bool = False) -> str:
        pass

    def validate(self, verbose: bool = False) -> None:
        pass

    def encoding(self) -> str:
        return PARITY_2D_ENCODE
