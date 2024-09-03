import logging
from time import sleep
from serial import serial_for_url
from serial.serialutil import SerialException
from serial.tools.list_ports import comports

from python.comm_base import STM32_COM_BASE
from python.command import Command
from python.message import Message


INTERFACE_NAME = "STM32_UART"
BAUD = 115200
HWID = "0403:6001"


class STM32ConnectionError(Exception):
    """Failed to Connect to the Adapter..."""


class STM32_UART(STM32_COM_BASE):
    """Communicate with STM32 via UART.

    Uses the SH-U09C5 USB to TTL Adapter.
    https://www.deshide.com/product-details.html?pid=303205&_t=1661493660

    """

    def __init__(self, name: str = INTERFACE_NAME, hwid: str = HWID, baud=BAUD):
        self.hwid = hwid
        self.baud = baud
        super().__init__(name)

    def connect(self):
        """
        Connect to the STM32 via UART.

        Raises:
            STM32ConnectionError: We Failed to connect via UART.
        """
        self.logger.info(f"Connecting to STM32 via hwid {self.hwid}")
        try:
            self.ser = serial_for_url(f"hwgrep://{self.hwid}", self.baud)
            self.ser.timeout = 1
        except SerialException:
            self.logger.error(f"Failed to find USB TTL Adapter....")
            self.logger.info("Only Found:")
            for port in comports():
                self.logger.info(
                    f"\tDescription: {port.description}, HWID: {port.hwid}"
                )
            raise STM32ConnectionError(
                "Failed to Find the UART Adapter... Is HWID correct?"
            )
        self.logger.info(f"Connection Successful")

    def read(self):
        """
        Read a message from the STM32
        """
        ret = self.ser.read(Message.dtype.itemsize)
        self.logger.debug(f"Received {ret}")
        msg: Message = Message.load(ret)
        self.logger.info(f"Received message: {msg}")

    def exchange(self, msg: Message) -> Message:
        """
        Send a message and obtain a response.

        Args:
            msg (Message): message to send.

        Returns:
            Message: response message.
        """
        self.logger.info(f"Sending {msg}")
        self.ser.write(bytes(msg))
        ret = self.ser.read(Message.dtype.itemsize)
        self.logger.debug(f"Received Response {ret}")
        ret_msg: Message = Message.load(ret)
        self.logger.info(f"Received Response: {ret_msg}")
        return ret_msg

    def teardown(self):
        self.ser.close()


if __name__ == "__main__":
    stm32 = STM32_UART()
    our_msg = Message(Command.HELLO, 1235)
    nok_msg = Message(Command.NOK, 1234)
    while True:
        our_msg = stm32.exchange(our_msg)
        stm32.exchange(nok_msg)
        sleep(1)
