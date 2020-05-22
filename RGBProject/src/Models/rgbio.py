class frame:
    _s_Byte = b'\x02'
    _e_Byte = b'\x03' # [s_Byte][length][mode][config][data(max 8 bytes)][CRC-A][CRC-B][e_Byte]
    _max_data_len = 8

    TURN_ON = 66
    FIRE = 117
    GET_STATUS = 83
    TURN_OFF = 69


    """ Specifies a frame structure
        --->mode
        66 -> turn on
        117-> fire
        83-> get status
        69-> turn off   
        :param config: this byte is used for configuration of to frame:
                       first bit is specifies if the crc check is performed. Rest of the bits
                       are reserved for later use. 
                       Example:
                       crc_active = True --> config = 00000001                         
    """
    def __init__(self, mode, data=None, crc_active=False):
        """
        :param data: a custom data consisting of 0 to 8 bytes
        :param crc_active: is crc operation performed(Suggested)
        TODO implement HSV color space
        """
        if data is None:
            data = [0]
        if len(data) > self.__class__._max_data_len:
            raise ValueError('max data length exceed which is {}'.format(self.__class__._max_data_len))

        self.mode = mode.to_bytes(1, "big", signed=False)
        self.data = data
        self.data_as_bytes = bytes(data)
        self.length = int(len(data)+7).to_bytes(1, "big", signed=False)         # TODO throw custom exceptions with _validateVal static method
        self.crc_active = crc_active

    # def _validateVal()

    # define getters
    def get_RGB(self):
        """
        :return: a tuple of R G B values in type of int
        """
        return int.from_bytes(self.data[0], 'big', signed=False), int.from_bytes(self.data[1], 'big', signed=False), int.from_bytes(self.data[2], 'big', signed=False)

    def get_config_as_Bytes(self):
        a = [False, False, False, False, False, False, False, self.crc_active]
        return int(''.join('1' if i else '0' for i in a), 2).to_bytes(1, 'big', signed=False)

    def get_CRC_as_Bytes(self):
        s= 0
        for i in self.data:
            s += i
        return s.to_bytes(2, 'big', signed=False)

    def as_bytes(self):
            return self.__class__._s_Byte + \
                   len(self.data).to_bytes(1, "big", signed=False) + \
                   self.mode + \
                   self.get_config_as_Bytes() + \
                   self.data_as_bytes + \
                   self.get_CRC_as_Bytes() + \
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

class led:
    port = "COM10"
    baudrate = 9600

    def __init__(self):
        self.handle = serial.Serial(self.__class__.port, self.__class__.baudrate, parity=serial.PARITY_NONE)

    def close_com(self):
        if not self.handle.is_open:
            print("port is already closed")
        else:
            self.handle.close()

    def open_com(self):
        if self.handle.is_open:
            print("port is already open")
        else:
            self.handle.open()

    #TODO heartbeat handshake


    def turn_on(self):
        f = frame(frame.TURN_ON)
        self.handle.write(f.as_bytes())

    def turn_off(self):
        f = frame(frame.TURN_OFF)
        self.handle.write(f.as_bytes())

    def fire_with_color(self, color):
        """
        fires led in specified color
        :param color: "red", "green", "blue" or an rgb value in 3 tuple format
        :return:
        """
        if color == "red":
            rgb = (255, 0, 0)
        elif color == "green":
            rgb = (0, 255, 0)
        elif color == "blue":
            rgb = (0, 0, 255)
        else:
            rgb = color

        f = frame(frame.FIRE, [rgb[0], rgb[1], rgb[2]])
        self.handle.write(f.as_bytes())

    #TODO LOG system
    #TODO changing name conventions (like fire_with_color)
    #TODO fixing voltage requlation





