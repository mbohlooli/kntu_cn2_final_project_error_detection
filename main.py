from Packetizer import Packetizer
from HammingEncoder import HammingEncoder

if __name__ == '__main__':
    packetizer = Packetizer(HammingEncoder(16))
    packets = packetizer.packetize('hello world!')

    packets[1].message[7] = 1 - packets[1].message[7]
    packets[2].message[9] = 1 - packets[2].message[9]

    received_message = packetizer.de_packetize(packets, False, True)

    print(f'data of the packet: {received_message}')
