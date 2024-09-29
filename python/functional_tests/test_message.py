import numpy as np
import pytest

from python.command import Command
from python.command_map import CMD_TO_DTYPE
from python.message import Message, MessageHeader, COMMAND


def test_equality():
    # Test different messages
    msg_1 = Message(Command.HELLO, [12345])
    msg_2 = Message(Command.HELLO, [12346])
    assert msg_1 != msg_2
    # Test same messages
    msg_2 = Message(Command.HELLO, [12345])
    assert msg_1 == msg_2
    # Test random object
    assert msg_1 != 1


def test_message_header():
    cmd = Command.HELLO
    data = [1, 2, 3, 4, 5]
    msg_header_1 = MessageHeader.load_from_args(cmd, data)
    raw_bytes = bytes(msg_header_1)

    msg_header_2 = MessageHeader.load(raw_bytes)

    assert np.array_equal(msg_header_1._ar, msg_header_2._ar)
    assert msg_header_1.data_dtype == msg_header_2.data_dtype


# Test different message types and lengths for serialization and deserialization
@pytest.mark.parametrize(
    "command, data",
    [
        (Command.HELLO, [1, 2, 3, 4, 5]),
        (Command.HELLO, [i for i in range(127)]),
        (Command.NOK, [255]),
        (Command.NOK, [i for i in range(255)]),
        (Command.TIME, [1234567890]),
        (Command.TIME, [1234567890 + i for i in range(20)]),
    ],
)
def test_message(command, data):
    # Test Message construction from command and data
    msg_from_args = Message(command, data)
    assert (
        msg_from_args.message_header.payload_size[0]
        == len(data) * CMD_TO_DTYPE[msg_from_args.command]().itemsize
    )

    # Create raw bytes manually
    _bytes = b""
    _bytes += bytes(np.array([command.value], dtype=MessageHeader.dtype[COMMAND]))
    _bytes += bytes(
        np.array([len(data) * CMD_TO_DTYPE[command]().itemsize], dtype=np.uint8)
    )
    _bytes += bytes(np.array(data, dtype=CMD_TO_DTYPE[command]))

    # Load message from raw bytes
    msg_from_bytes = Message.load(_bytes)

    # Assert that the two messages (from args and bytes) are the same
    assert msg_from_args == msg_from_bytes

    # Test serialize -> deserialize roundtrip
    raw_data = bytes(msg_from_args)
    loaded_msg = Message.load(raw_data)
    assert loaded_msg == msg_from_args
    assert np.array_equal(data, loaded_msg.data)


# TODO: We should also test edge cases -> messages with too large of payloads (payload size is uint8!)
