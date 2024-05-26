from MessageBlock import *
from Packetizer import Packetizer

if __name__ == '__main__':
    packetizer = Packetizer()
    packets = packetizer.packetize('lo')

    packets[1].message[7] = 1 - packets[1].message[7]

    received_message_bin = ''
    for index, packet in enumerate(packets):
        print(f'Packet {index + 1} - ', end='')
        if not packet.validate(True):
            print(f'Error Detected at packet {index + 1}')
        received_message_bin += packet.read()

    received_message = ''.join(
        chr(int(received_message_bin[i:i + 8], 2)) for i in range(0, len(received_message_bin), 8))

    print(f'data of the packet: {received_message}')
