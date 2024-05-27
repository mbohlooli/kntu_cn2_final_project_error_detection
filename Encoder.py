from abc import ABC, abstractmethod


class Encoder(ABC):
    def __init__(self, block_size: int):
        self.block_size = block_size
        self.max_data_size = block_size

    @abstractmethod
    def encode(self, data: str, block: list[int], verbose: bool = False) -> None:
        pass

    @abstractmethod
    def decode(self, block: list[int], fix_inplace: bool = False, verbose: bool = False) -> str:
        pass

    @staticmethod
    @abstractmethod
    def validate(block: list[int], inplace: bool = False, verbose: bool = False) -> bool:
        pass
