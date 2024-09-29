import numpy as np
from numpy.typing import ArrayLike
from python.command import Command
from python.command_map import CMD_TO_DTYPE
from typing import Optional

COMMAND = "command"
DATA = "data"
PAYLOAD_SIZE = "payload_size"


class MessageHeader:
    """Header for the Message which includes info about the message structure."""

    dtype: np.dtype = np.dtype(
        [
            (COMMAND, np.uint8),  # Commands will map 1:1 to data types
            (PAYLOAD_SIZE, np.uint8),  # Number of bytes in the message
        ]
    )

    def __init__(self, ar: np.ndarray):
        self._ar = ar
        self.command = Command(self._ar[COMMAND])
        self.payload_size = self._ar[PAYLOAD_SIZE]
        self.data_dtype = CMD_TO_DTYPE[self.command]

    @classmethod
    def load(cls, input_bytes: bytes) -> "MessageHeader":
        """
        Load the MessageHeader from raw bytes.

        Args:
            input_bytes (bytes): bytes which contain the MessageHeader at the start. Can contain extra bytes.

        Returns:
            MessageHeader: A messageHeader object generated from the bytes.
        """
        return cls(np.frombuffer(input_bytes[: cls.dtype.itemsize], dtype=cls.dtype))

    @classmethod
    def load_from_args(cls, cmd: Command, data: ArrayLike) -> "MessageHeader":
        """
        Load the Message directly from command and data.

        Args:
            cmd (Command): Command of the Message.
            data (ArrayLike): Data of the Message.

        Returns:
            MessageHeader: A messageHeader object generated from the command and data.
        """
        data_dtype = CMD_TO_DTYPE[cmd]
        data_len = len(data)
        payload_size = data_len * data_dtype().itemsize
        return cls(np.array([(cmd.value, payload_size)], dtype=cls.dtype))

    def __bytes__(self) -> bytes:
        return bytes(self._ar)

    def __str__(self) -> str:
        return (
            f"MessageHeader: Command: {self.command} Payload Size {self.payload_size}"
        )


class Message:

    def __init__(self, cmd: Command, data: ArrayLike):
        """
        Generate a message with optional command and data.

        Args:
            cmd (Command): Command of the message.
            data (ArrayLike): Data of the Message.
        """
        self.message_header: MessageHeader = MessageHeader.load_from_args(cmd, data)
        self._data = np.array(data, dtype=self.message_header.data_dtype)

    def __new__(cls, msg_header: MessageHeader, data: ArrayLike) -> "Message":
        """
        Create a new Message without init.

        Args:
            msg_header (MessageHeader): MessageHeader of the message.
            data (ArrayLike): Data of the message.

        Returns:
            Message: The message instance
        """
        inst = super(Message, cls).__new__(cls)
        inst.message_header = msg_header
        inst._data = data
        return inst

    @classmethod
    def load(cls, data: bytes) -> "Message":
        """
        Load a Message from bytes.

        Args:
            data (bytes): bytes of the message.

        Returns:
            Message: The loaded Message.
        """
        msg_header = MessageHeader.load(data)
        data = np.frombuffer(
            data[
                msg_header.dtype.itemsize : msg_header.dtype.itemsize
                + msg_header.payload_size[0]
            ],
            dtype=msg_header.data_dtype,
        )
        # We don't really want to init, so use __new__
        return cls.__new__(cls, msg_header, data)

    @property
    def command(self) -> Command:
        """
        Return the command and not the enum value.

        Returns:
            Command: stored command.
        """
        return self.message_header.command

    @property
    def data(self):
        """
        Return the stored data.

        Returns:
            np.ndarray: Array of data in the message/
        """
        return self._data

    def __str__(self):
        return f"""Message:
    Command: {self.command}\t Data: {self._data}"""

    def __bytes__(self):
        return bytes(self.message_header) + bytes(self._data)

    def bytes_uart(self):
        # Combine header and data
        message_bytes = bytes(self.message_header) + bytes(self._data)

        # Calculate how many bytes are needed to pad the message to 256 bytes
        padding_length = 256 - len(message_bytes)

        # Pad the message with zeros (or any other padding value if needed)
        if padding_length > 0:
            message_bytes += b"\x00" * padding_length

        return message_bytes

    def __eq__(self, other):
        if not isinstance(other, Message):
            return False

        # Check if the command and data fields are equal
        cmd_equal = self.command == other.command
        return cmd_equal and np.array_equal(self._data, other._data)
