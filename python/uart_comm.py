import logging
from time import sleep
from serial import serial_for_url
from serial.serialutil import SerialException
from serial.tools.list_ports import comports

from python.comm_base import STM32_COM_BASE
from python.command import Command
from python.message import Message, MessageHeader


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
        ret = self.ser.read(MessageHeader.dtype.itemsize)
        self.logger.debug(f"Received Header Bytes {ret}")
        header = MessageHeader.load(ret)
        payload = self.ser.read(header.payload_size)
        self.logger.debug(f"Received Payload Bytes {payload}")
        msg: Message = Message.load(ret + payload)
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

        msg_bytes = bytes(msg)
        self.logger.debug(f"Sending {msg_bytes}")
        # Write the header
        self.ser.write(msg_bytes[: MessageHeader.dtype.itemsize])
        # Write the data
        self.ser.write(msg_bytes[MessageHeader.dtype.itemsize :])
        ret_msg = self.recv_msg()
        self.logger.info(f"Received Response: {ret_msg}")
        return ret_msg

    def recv_msg(self) -> Message:
        """
        Receive a message in two parts, first the header, then the data.

        Returns:
            Message: Constructed message object.
        """

        ret = self.ser.read(MessageHeader.dtype.itemsize)
        self.logger.debug(f"Received Response {ret}")
        header = MessageHeader.load(ret)
        # Read the payload
        data = self.ser.read(int(header.payload_size[0]))
        self.logger.debug(f"Received data {data}")
        return Message.load(ret + data)  # TODO youre deserializing the header 2x

    def teardown(self):
        self.ser.close()


if __name__ == "__main__":
    import logging

    logging.getLogger().setLevel(logging.DEBUG)
    stm32 = STM32_UART()
    hello = Message(
        Command.HELLO,
        [
            5,
            5,
            5,
            5,
        ],
    )
    while True:
        ret_msg = stm32.exchange(hello)
        hello = ret_msg
        sleep(1)
