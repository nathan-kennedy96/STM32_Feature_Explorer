from abc import ABC, abstractmethod
import socket
import logging
from time import sleep
from datetime import datetime, UTC
from python.command import Command
from python.message import Message

INTERFACE_NAME = "STM32_COM_BASE"


class STM32_COM_BASE(ABC):

    def __init__(
        self,
        name: str = INTERFACE_NAME,
    ):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(name)
        self.connect()

    @abstractmethod
    def connect(self) -> None:
        """
        Connect to the STM32 via the interface.
        """

    @abstractmethod
    def teardown(self) -> None:
        """
        Close the connection if it exists.
        """

    @abstractmethod
    def exchange(self, msg: Message) -> Message:
        """
        Send a message and return the response.

        Args:
            msg (Message): Message to send.

        Returns:
            Message: Response Message
        """

    def get_time(self) -> datetime:
        """
        Get the Time from STM32

        Returns:
            datetime: Time Returned by STM32
        """
        resp = self.exchange(Message(Command.TIME, 0))
        dt = datetime.fromtimestamp(resp.data[0], UTC)
        self.logger.info(f"DateTime Received: {dt}")
        return dt

    def set_time(self, dt: datetime) -> datetime:
        """
        Set the Time on STM32

        Args:
            dt (datetime): Time to set.

        Returns:
            datetime: datetime returned after setting.
        """
        resp = self.exchange(Message(Command.TIME, int(dt.timestamp())))
        dt = datetime.fromtimestamp(resp.data[0], UTC)
        self.logger.info(f"DateTime Received: {dt}")
        return dt
