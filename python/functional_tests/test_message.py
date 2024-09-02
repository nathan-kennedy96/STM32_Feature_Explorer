from python.command import Command
from python.message import Message


def test_equality():
    # Test different messages
    msg_1 = Message(Command.HELLO, 12345)
    msg_2 = Message(Command.HELLO, 12346)
    assert msg_1 != msg_2
    # Test same messages
    msg_2 = Message(Command.HELLO, 12345)
    assert msg_1 == msg_2
    # Test random object
    assert msg_1 != 1
