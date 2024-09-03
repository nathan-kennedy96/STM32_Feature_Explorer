import socket
import logging
from time import sleep
from datetime import datetime
from python.command import Command
from python.message import Message
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
        self.sock.sendall(bytes(msg))
        ret = self.sock.recv(Message.dtype.itemsize)
        self.logger.debug(f"Received Response {ret}")
        ret_msg: Message = Message.load(ret)
        self.logger.info(f"Received Response: {ret_msg}")
        return ret_msg


if __name__ == "__main__":
    stm32_tcp = STM32_TCP()
    time_msg = Message(Command.TIME, 0)
    while True:

        stm32_tcp.set_time(datetime(year=2000, month=2, day=1))
        sleep(5)
        stm32_tcp.get_time()
