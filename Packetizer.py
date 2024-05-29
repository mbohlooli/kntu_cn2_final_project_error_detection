from abc import ABC, abstractmethod

from Encoder import Encoder
from MessageBlock import MessageBlock


class Packetizer(ABC):
    def __init__(self, encoder: Encoder):
        self.encoder = encoder
        self.packet_size = encoder.block_size

    @abstractmethod
    def packetize(self, packet_data: str) -> list[MessageBlock]:
        pass

    @staticmethod
    @abstractmethod
    def de_packetize(packets: list[MessageBlock], fix_errors: bool = True, verbose: bool = False) -> str:
        pass
