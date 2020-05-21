class frame:
    _s_Byte = b'\x02'
    _e_Byte = b'\x03'
    _f_length = 8  # [s_Byte][config][R][G][B][CRC-A][CRC-B][e_Byte]
    """ Specifies a frame structure
        :param config: this byte is used for configuration of to frame:
                       first bit is specifies if the crc check is performed. Rest of the bits
                       are reserved for later use. 
                       Example:
                       crc_active = True --> config = 00000001  
                            
    """

    def __init__(self, R, G, B, crc_active=True):
        """
        :param R: Red Channel Value
        :param G: Green Channel Value
        :param B: Blue Channel Value
        :param crc_active: is crc operation performed(Suggested)
        TODO implement HSV color space
        """
        self.R = int(R).to_bytes(1, "big", signed=False)  # TODO throw custom exceptions with _validateVal static method
        self.G = int(G).to_bytes(1, "big", signed=False)
        self.B = int(B).to_bytes(1, "big", signed=False)
        self.crc_active = crc_active

    # def _validateVal()

    # define getters
    def get_RGB(self):
        """
        :return: a tuple of R G B values in type of int
        """
        return int.from_bytes(self.R, 'big'), int.from_bytes(self.G, 'big'), int.from_bytes(self.B, 'big')

    def get_config_as_Bytes(self):
        a = [False, False, False, False, False, False, False, self.crc_active]
        return int(''.join('1' if i else '0' for i in a), 2).to_bytes(1, 'big', signed=False)

    def get_CRC_as_Bytes(self):
        r, g, b = self.get_RGB();
        s = r + g + b;
        return s.to_bytes(2, 'big', signed=False)

    def as_bytes(self):
        if self.crc_active:
            return self.__class__._s_Byte + \
                   self.get_config_as_Bytes() + \
                   self.R + self.G + self.B + \
                   self.get_CRC_as_Bytes() + \
                   self.__class__._e_Byte
        else:
            return self.__class__._s_Byte + \
                   self.get_config_as_Bytes() + \
                   self.R + self.G + self.B + \
                   b'\x00\x00' + \
                   self.__class__._e_Byte

    @staticmethod
    def unpack_config(val):
        """
        :param val: is a config byte in type of bytes
        :return: a list of booleans representing the configurations specified in the class documentation
        """
        as_str = bin(int.from_bytes(val, 'big'))[2:]
        config = list()
        for i in range(0, 8 - len(as_str)):
            config.append(False)
        for i in as_str:
            config.append(True if i == '1' else False)
        return config

    #TODO implement unpack bytes: converts bytes to list of integers
    #TODO implement from_bytes: converts bytes to Frame object

import serial

class connection:
    port = "COM10"
    baudrate = 9600

    def __init__(self):
        self.handle = serial.Serial(self.__class__.port, self.__class__.baudrate, parity=serial.PARITY_NONE)

    def initilize(self):
        self.handle.open()

