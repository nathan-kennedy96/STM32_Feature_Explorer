"""

Functional Test of eth communication.


"""


from python.eth_comm import STM32_TCP
from python.message import Message
from python.command import Command

class TestTCPFunctionality:

    def setup_method(self):
        self.stm_32_tcp = STM32_TCP()

    def teardown_method(self):
        self.stm_32_tcp.teardown()

    def test_hello_message(self):
        """ Test that the hello message returns a response with correct Command and data"""
        data_number = 1234
        hello_msg = Message(Command.HELLO, data_number)
        response_message = self.stm_32_tcp.exchange(hello_msg)
        #Hello is programmed to respond with data incremented by one
        assert response_message.data == data_number+1

    def test_nok_message(self):
        """ Test that the nok message or unknown message responds with the expected NOK message."""
        nok_msg = Message(Command.NOK, 0)
        response_message = self.stm_32_tcp.exchange(nok_msg)
        assert response_message.data == 0
        assert response_message.command is Command.NOK
        assert response_message == nok_msg