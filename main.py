from HammingEncoder import HammingEncoder
from ReedSolomonPacketizer import ReedSolomonPacketizer
from SimpleEncoder import SimpleEncoder
from SimplePacketizer import SimplePacketizer

if __name__ == '__main__':
    encoding = input('Select the encoding:\na.Hamming\nb.Reed-Solomon\n')
    if encoding in ['a', 'b']:
        message = input('Enter the message: ')

    if encoding == 'a':
        packetizer = SimplePacketizer(HammingEncoder(16))
        packets = packetizer.packetize(message)

        packets[1].message[7] = 1 - packets[1].message[7]
        packets[2].message[9] = 1 - packets[2].message[9]

        print(f'Divided the message into {len(packets)} packets.')

        print(f'received data: {packetizer.de_packetize(packets, False, True)}')
        received_message = packetizer.de_packetize(packets, True, False)
        print(f'fixed data: {received_message}')
    elif encoding == 'b':
        packetizer = ReedSolomonPacketizer(SimpleEncoder(32))
        packets = packetizer.packetize(message)

        print(f'Divided the message into {len(packets)} packets.')

        packets.pop(len(packets)-2)

        print(f'received data: {packetizer.de_packetize(packets, False, True)}')
        received_message = packetizer.de_packetize(packets, True, False)

        print(f'fixed data: {received_message}')
    else:
        print('Invalid encoding')


