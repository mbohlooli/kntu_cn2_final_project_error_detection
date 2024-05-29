from Encoder import Encoder
from MessageBlock import MessageBlock, ArrayMessageBlock
from Packetizer import Packetizer
from scipy.interpolate import lagrange
from math import ceil


class ReedSolomonPacketizer(Packetizer):
    def __init__(self, encoder: Encoder, max_fault: int = 2):
        super().__init__(encoder)
        self.max_fault = max_fault
        self.packets_count = 0

    def packetize(self, packet_data: str) -> list[MessageBlock]:
        bin_data = ''.join(format(ord(x), '08b') for x in packet_data)

        data_chunks = []
        for i in range(0, len(bin_data), self.encoder.max_data_size):
            data_chunks.append(bin_data[i:i + self.encoder.max_data_size])

        numeric_values = list(map(lambda data: int(''.join(data), 2), data_chunks))
        indexes = [i for i in range(len(numeric_values))]

        polynomial = lagrange(indexes, numeric_values)

        extra_packets = [
            int(polynomial(i)) for i in range(len(numeric_values), len(numeric_values) + self.max_fault)
        ]
        numeric_values += extra_packets

        next_index = len(numeric_values) - len(extra_packets)
        for i in range(self.max_fault):
            indexes.append(i + next_index)

        packets = []
        for index, value in zip(indexes, numeric_values):
            bin_value = format(value, f'0{self.encoder.block_size}b')
            packets.append(ArrayMessageBlock(self.encoder, bin_value, index))

        self.packets_count = len(packets)
        return packets

    def de_packetize(self, packets: list[MessageBlock], fix_errors: bool = True, verbose: bool = False) -> str:
        indexes = []
        numeric_values = []

        if len(packets) < self.packets_count - self.max_fault:
            print('Unable to reconstruct missing packets due to high packet loss.')
            return ''

        if len(packets) != self.packets_count:

            while len(packets) > self.packets_count - self.max_fault:
                packets.pop(0)

            block_size = packets[0].encoder.block_size
            encoder = packets[0].encoder

            for packet in packets:
                indexes.append(packet.seq_number)
                bin_value = ('-' if packet.sign == '-' else '') + ''.join(map(str, packet.message))
                value = int(bin_value, 2)
                numeric_values.append(value)

            polynomial = lagrange(indexes, numeric_values)

            index = 0
            packets_to_insert = []
            for packet in packets:
                if packet.seq_number != index:
                    if verbose:
                        print(f'packet number {index+1} missing - reconstructing ...')

                    numeric_value = ceil(polynomial(index))
                    numeric_values.insert(index, numeric_value)
                    bin_value = format(numeric_value, f'0{block_size}b')
                    if fix_errors:
                        packets_to_insert.append((index, ArrayMessageBlock(encoder, bin_value, index)))
                    index += 1

                index += 1

            for packet_to_insert in packets_to_insert:
                packets.insert(packet_to_insert[0], packet_to_insert[1])

        received_message_bin = ''
        for index, packet in enumerate(packets):
            if verbose:
                print(f'Packet {index + 1} - ', end='')
            if not packet.validate(fix_errors, verbose) and verbose:
                print(f'Error {"fixed" if fix_errors else "at"} at packet {index + 1}')
            if index < len(packets) - self.max_fault:
                received_message_bin += packet.read()

        return ''.join(
            chr(int(received_message_bin[i:i + 8], 2)) for i in range(0, len(received_message_bin), 8))

    @staticmethod
    def _is_prime(number: int) -> bool:
        for n in range(2, int(number ** 0.5) + 1):
            if number % n == 0:
                return False
        return True
