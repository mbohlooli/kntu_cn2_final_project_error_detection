from abc import ABC, abstractmethod
from Encoder import Encoder


class MessageBlock(ABC):
    def __init__(self, encoder: Encoder, seq_number: int = 0, sign: str = '+'):
        self.encoder = encoder
        self.seq_number = seq_number
        self.sign = sign

    @abstractmethod
    def write(self, data: str, verbose: bool = False) -> None:
        pass

    @abstractmethod
    def read(self, verbose: bool = False) -> str:
        pass

    @abstractmethod
    def validate(self, verbose: bool = False, inplace: bool = False) -> None:
        pass


class ArrayMessageBlock(MessageBlock):
    def __init__(self, encoder: Encoder, data='', seq_number: int = 0, sign: str = '+'):
        super().__init__(encoder, seq_number, sign)
        self.block_size = encoder.block_size
        self.message = [0 for _ in range(self.block_size)]

        if len(data) > 0:
            self.write(data)

    def write(self, data: str, verbose: bool = False) -> None:
        if data[0] == '-':
            self.sign = '-'
            data = data[1:]
        self.encoder.encode(data, self.message, verbose)

    def read(self, fix_inplace: bool = False, verbose: bool = False) -> str:
        return ('-' if self.sign == '-' else '') + self.encoder.decode(self.message, fix_inplace, verbose)

    def validate(self, inplace: bool = False, verbose: bool = False) -> bool:
        return self.encoder.validate(self.message, inplace, verbose)

    def __str__(self):
        return ''.join(map(str, self.message))
