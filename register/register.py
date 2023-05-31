# Micropython library that provides a convenient and efficient way to interact
# with registers and manipulate individual bits of devices connected to the
# Serial Peripheral Interface (SPI).
#
# Access and control the values of registers, perform read and write operations,
# and manipulate specific bits within a register.
#
# The library abstracts the low-level details of SPI communication, allowing
# users to focus on working with registers and bits.
#
# Key Features:
# - Simple and intuitive API
# - Read and write operations on registers
# - Bit-level manipulation and access within registers
# 
# Author: Chris Braissant
# License: MIT

from machine import SPI, Pin

class Bits:
    """
    A class representing a set of bits within a register.

    Args:
        register_address (int): The address of the register.
        start_position (int): The starting bit position within the register.
        length (int, optional): The number of bits. Defaults to 1.
    """
    def __init__(self, register_address, start_position:int, length:int = 1):
        self.register_address = register_address
        self.start_position = start_position
        self.length = length
        self.mask = ((1 << self.length) - 1) << self.start_position

    def __get__(self, obj, objtype=None):
        reg = Register(self.register_address, 1)
        data = reg.__get__(obj)
        data &= self.mask
        data >>= self.start_position
        return data 

    def __set__(self, obj, value):
        reg = Register(self.register_address, 1)
        data = reg.__get__(obj)
        # clear the bits to write
        data &= ~self.mask 
        # write the new value
        data |= (value << self.start_position)
        reg.__set__(obj, data)



class Register:
    '''
    A class representing a register for SPI communication.

    Args:
        register_address (int): The address of the register.
        length (int, optional): The length of the register in bytes. Defaults to 1.
    '''
    def __init__(self, register_address:int, length:int = 1):
        self.register_address = register_address
        self.length = length
    
    def start_transaction(self, obj, objtype=None):
        obj.cs.value(0)
    
    def end_transaction(self, obj, objtype=None):
        obj.cs.value(1)

    def convert_bytes_to_int(self, bytes):
        return int.from_bytes(bytes, 'little')
    
    def convert_int_to_bytes(self, data):
        return data.to_bytes(self.length, 'little')
            
    def __get__(self, obj, objtype=None):
        msg = bytearray()
        msg.append(0x80 | self.register_address)
        self.start_transaction(obj)
        obj.spi.write(msg)
        data = obj.spi.read(self.length)
        self.end_transaction(obj)
        return self.convert_bytes_to_int(data)

    def __set__(self, obj, data):
        data_bytes = self.convert_int_to_bytes(data)
        msg = bytearray()
        msg.append(self.register_address)
        msg.extend(data_bytes)
        self.start_transaction(obj)
        obj.spi.write(msg)
        self.end_transaction(obj)