from MessageBlock import *

if __name__ == '__main__':
    message_block: MessageBlock = ArrayMessageBlock(block_size=32)
    message_block.write('11101001000', True)
    message_block.read(True)
