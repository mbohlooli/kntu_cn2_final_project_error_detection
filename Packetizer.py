from MessageBlock import MessageBlock, ArrayMessageBlock
from math import log2


class Packetizer:
    def __init__(self, packet_size=16):
        self.packet_size = packet_size

    def packetize(self, packet_data: str) -> list[MessageBlock]:
        data_in_packet_size = self.packet_size - 1 - int(log2(self.packet_size))

        data_chunks = []
        for i in range(0, len(packet_data), data_in_packet_size):
            data_chunks.append(packet_data[i:i + data_in_packet_size])

        return list(map(lambda data: ArrayMessageBlock(data=data), data_chunks))
