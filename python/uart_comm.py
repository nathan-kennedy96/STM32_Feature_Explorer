import logging
import numpy as np
from time import sleep
from serial import serial_for_url
from serial.serialutil import SerialException
from serial.tools.list_ports import comports

from command import Command

logging.basicConfig(level=logging.DEBUG)

INTERFACE_NAME = "STM32"
BAUD = 115200
HWID = "0403:6001"

class STM32ConnectionError(Exception):
    """Failed to Connect to the Adapter..."""

class Message: 
    #TODO: can this dtype be inferred from the struct/c code?
    dtype: np.dtype =  np.dtype([
    ("command", np.int16),
    ("data", np.uint16),
    ]) 

    def __init__(self, cmd: Command = None, data: int = None):
        if cmd is None:
            self._ar = np.array([], dtype=self.dtype)
        else:
            self._ar = np.array([(cmd.value,data)], dtype=self.dtype)


    
    @classmethod
    def load(cls, data: bytes):
        msg = cls(None, None)
        msg._ar = np.frombuffer(data, dtype=Message.dtype)
        return msg 
    @property
    def command(self):
        return self._ar["command"]

    @property
    def data(self):
        return self._ar["data"]
    
    def __str__(self):
        return f"Command: {self.command}\t Data: {self.data}"

    def __bytes__(self):
        return bytes(self._ar)
    

class STM32_UART:
    """Communicate with STM32 via UART.
    
    Uses the SH-U09C5 USB to TTL Adapter.
    https://www.deshide.com/product-details.html?pid=303205&_t=1661493660

    """

    def __init__(self, name: str = INTERFACE_NAME, hwid: str = HWID):
        self.logger = logging.getLogger(name)
        self.logger.info(f"Connecting to STM32 via hwid {hwid}")
        try:
            self.ser = serial_for_url(f"hwgrep://{hwid}", baudrate=BAUD)
            self.ser.timeout = 1
        except SerialException:
            self.logger.error(f"Failed to find USB TTL Adapter....")
            self.logger.info("Only Found:")
            for port in comports():
                self.logger.info(f"\tDescription: {port.description}, HWID: {port.hwid}")
            raise STM32ConnectionError("Failed to Find the UART Adapter... Is HWID correct?")
        self.logger.info(f"Connection Successful")


    def read(self):
        """
        Read a message from the STM32
        """
        ret = self.ser.read(Message.dtype.itemsize)
        self.logger.debug(f"Received {ret}")
        msg: Message = Message.load(ret)
        self.logger.info(f"Received message: {msg}")

    def _exchange(self, msg: Message) -> Message:
        self.logger.info(f"Sending {msg}")
        self.ser.write(bytes(msg))
        ret = self.ser.read(Message.dtype.itemsize)
        self.logger.debug(f"Received Response {ret}")
        ret_msg: Message = Message.load(ret)
        self.logger.info(f"Received Response: {ret_msg}")
        return ret_msg
        



if __name__ == "__main__":
    stm32 = STM32_UART()
    our_msg = Message(Command.HELLO, 1235)
    nok_msg = Message(Command.NOK, 1234)
    while True:
        our_msg = stm32._exchange(our_msg)
        stm32._exchange(nok_msg)
        sleep(1)