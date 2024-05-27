from abc import ABC, abstractmethod
from Encoder import Encoder


class MessageBlock(ABC):
    def __init__(self, encoder: Encoder):
        self.encoder = encoder

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
    def __init__(self, encoder: Encoder, data=''):
        super().__init__(encoder)
        self.block_size = encoder.block_size
        self.message = [0 for _ in range(self.block_size)]

        if len(data) > 0:
            self.write(data)

    def write(self, data: str, verbose: bool = False) -> None:
        self.encoder.encode(data, self.message, verbose)
        # if self.en == HAMMING_ENCODE:
        #     self._write_hamming(data, verbose)

    def read(self, fix_inplace:bool = False, verbose: bool = False) -> str:
        return self.encoder.decode(self.message, fix_inplace, verbose)
        # if self.encoding == HAMMING_ENCODE:
        #     return self._read_hamming(verbose)

    def validate(self, inplace: bool = False, verbose: bool = False) -> bool:
        return self.encoder.validate(self.message, inplace, verbose)
        # if self.encoding == HAMMING_ENCODE:
        #     return self._validate_message_hamming(verbose, inplace)
        # return False

    def __str__(self):
        return ''.join(map(str, self.message))
