from MessageBlock import *

if __name__ == '__main__':
    message_block: MessageBlock = ArrayMessageBlock()
    message_block.write('11101001000', True)
    message_block.message[1] = 0
    message_block.read(True)
