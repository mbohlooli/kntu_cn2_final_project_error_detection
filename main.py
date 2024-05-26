from MessageBlock import *
from Packetizer import Packetizer

if __name__ == '__main__':
    packetizer = Packetizer()
    packets = packetizer.packetize('1111111111100000000000111000')

    packets[1].message[7] = 1 - packets[1].message[7]

    for index, packet in enumerate(packets):
        print(f'Packet {index+1} - ', end='')
        if not packet.validate(True):
            print(f'Error Detected at packet {index+1}')
    # print(list(map(lambda x: x.read(), a)))
    # message_block: MessageBlock = ArrayMessageBlock()
    # message_block.write('11101001000', True)
    # message_block.message[1] = 0
    # message_block.read(True)
