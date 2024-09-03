import numpy as np
from python.command import Command
from typing import Optional

COMMAND = "command"
DATA = "data"


class Message:
    # TODO: can this dtype be inferred from the struct/c code?
    dtype: np.dtype = np.dtype(
        [
            (COMMAND, np.int16),
            (DATA, np.uint32),
        ]
    )

    def __init__(self, cmd: Optional[Command] = None, data: Optional[int] = None):
        """
        Generate a message with optional command and data.

        Args:
            cmd (Optional[Command], optional): Command of the message.. Defaults to None.
            data (Optional[int], optional): Data of the Message. Defaults to None.
        """
        if cmd is None:
            self._ar = np.array([], dtype=self.dtype)
        else:
            self._ar = np.array([(cmd.value, data)], dtype=self.dtype)

    @classmethod
    def load(cls, data: bytes) -> "Message":
        """
        Load a Message from bytes.

        Args:
            data (bytes): bytes of the message.

        Returns:
            Message: The loaded Message.
        """
        msg = cls(None, None)
        msg._ar = np.frombuffer(data, dtype=Message.dtype)
        return msg

    @property
    def command(self) -> Command:
        """
        Return the command and not the enum value.

        Returns:
            Command: stored command.
        """
        return Command(self._ar[COMMAND][0])

    @property
    def data(self):
        """
        Return the stored data.

        Returns:
            np.ndarray: Array of data in the message/
        """
        return self._ar[DATA]

    def __str__(self):
        return f"Command: {self.command}\t Data: {self.data}"

    def __bytes__(self):
        return bytes(self._ar)

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False

        # Check if the command and data fields are equal
        return np.array_equal(self._ar, other._ar)
