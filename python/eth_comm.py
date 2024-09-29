import socket
from time import sleep
from datetime import datetime
from python.command import Command
from python.message import Message, MessageHeader
from python.comm_base import STM32_COM_BASE

DEFAULT_HOST = "192.168.0.10"
DEFAULT_PORT = 12345
INTERFACE_NAME = "STM32_TCP"


class STM32_TCP(STM32_COM_BASE):

    def __init__(
        self,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        name: str = INTERFACE_NAME,
    ):
        self.host = host
        self.port = port
        self.sock = None
        self.timeout = 1
        super().__init__(name)

    def connect(self):
        """
        Connect to STM32 via tcp/ip
        """
        self.logger.info(f"Connecting to STM32 via TCP/IP at {self.host}:{self.port}")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))

    def teardown(self):
        """
        Close the connection if it exists.
        """
        if self.sock is not None:
            self.sock.close()
            self.sock = None

    def exchange(self, msg: Message) -> Message:
        """
        Send a message and return the response.

        Args:
            msg (Message): Message to send.

        Returns:
            Message: Response Message
        """
        self.logger.info(f"Sending {msg}")
        self.logger.debug(f"Sending bytes {bytes(msg)}")
        self.sock.sendall(bytes(msg))
        ret_msg = self.recv_msg()
        self.logger.info(f"Received Response: {ret_msg}")
        return ret_msg

    def recv_msg(self) -> Message:
        """
        Receive a message in two parts, first the header, then the data.

        Returns:
            Message: Constructed message object.
        """
        header_bytes = self.sock.recv(MessageHeader.dtype.itemsize)
        self.logger.debug(f"Received Header Bytes: {header_bytes}")
        msg_header = MessageHeader.load(header_bytes)
        self.logger.debug(f"Parsed Header: {msg_header}")
        payload_bytes = self.sock.recv(msg_header.payload_size[0])
        self.logger.debug(f"Received Payload Bytes: {payload_bytes}")
        return Message.load(
            header_bytes + payload_bytes
        )  # TODO youre deserializing the header 2x


if __name__ == "__main__":
    import logging

    logging.getLogger().setLevel(logging.DEBUG)
    stm32_tcp = STM32_TCP()
    # time_msg = Message(Command.TIME, 0)
    # while True:

    #     stm32_tcp.set_time(datetime(year=2000, month=2, day=1))
    #     sleep(5)
    #     stm32_tcp.get_time()
    hello = Message(Command.HELLO, [2, 3, 4, 5, 6])
    while True:
        ret_msg = stm32_tcp.exchange(hello)
        hello = ret_msg
        sleep(1)
