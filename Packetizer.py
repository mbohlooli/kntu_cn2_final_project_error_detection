from MessageBlock import MessageBlock, ArrayMessageBlock
from math import log2
import Encoder


class Packetizer:
    def __init__(self, encoder: Encoder):
        self.encoder = encoder
        self.packet_size = encoder.block_size

    def packetize(self, packet_data: str) -> list[MessageBlock]:
        bin_data = ''.join(format(ord(x), '08b') for x in packet_data)
        # data_in_packet_size = self.packet_size - 1 - int(log2(self.packet_size))

        data_chunks = []
        for i in range(0, len(bin_data), self.encoder.max_data_size):
            data_chunks.append(bin_data[i:i + self.encoder.max_data_size])

        return list(map(lambda data: ArrayMessageBlock(data=data, encoder=self.encoder), data_chunks))

    @staticmethod
    def de_packetize(packets: list[MessageBlock], fix_errors: bool = True, verbose: bool = False) -> str:
        received_message_bin = ''
        for index, packet in enumerate(packets):
            if verbose:
                print(f'Packet {index + 1} - ', end='')
            if not packet.validate(fix_errors, verbose) and verbose:
                print(f'Error {"fixed" if fix_errors else "at"} at packet {index + 1}')
            received_message_bin += packet.read()

        return ''.join(
            chr(int(received_message_bin[i:i + 8], 2)) for i in range(0, len(received_message_bin), 8))
