from MessageBlock import *
from Packetizer import Packetizer

if __name__ == '__main__':
    packetizer = Packetizer()
    packets = packetizer.packetize('lo')

    packets[1].message[7] = 1 - packets[1].message[7]

    received_message = packetizer.de_packetize(packets, True, True)

    print(f'data of the packet: {received_message}')
