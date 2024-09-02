from python.message import Message
from python.command import Command
from python.eth_comm import STM32_TCP
from python.uart_comm import STM32_UART
import pytest

class BaseTestCommFunctionality:

    @pytest.fixture(autouse=True)
    def setup_teardown(self, comm_interface):
        self.comm = comm_interface
        yield
        self.comm.teardown()

    @pytest.mark.parametrize("data_number, expected_response", [
        # Hello is programmed to respond with data incremented by one
        (1234, 1235),
        (0, 1),
        (999, 1000)
    ])
    def test_hello_message(self, data_number, expected_response):
        """Test that the hello message returns a response with correct Command and data"""
        hello_msg = Message(Command.HELLO, data_number)
        response_message = self.comm.exchange(hello_msg)
        assert response_message.data == expected_response

    @pytest.mark.parametrize("command, data, expected_command, expected_data", [
        (Command.NOK, 0, Command.NOK, 0),
        (Command.NOK, 123, Command.NOK, 0)
    ])
    def test_nok_message(self, command, data, expected_command, expected_data):
        """Test that the NOK message or unknown message responds with the expected NOK message."""
        nok_msg = Message(command, data)
        response_message = self.comm.exchange(nok_msg)
        assert response_message.data == expected_data
        assert response_message.command == expected_command
        assert response_message == Message(expected_command, expected_data)


@pytest.mark.usefixtures("comm_interface")
class TestTCPFunctionality(BaseTestCommFunctionality):

    @pytest.fixture
    def comm_interface(self):
        return STM32_TCP()


@pytest.mark.usefixtures("comm_interface")
class TestUARTFunctionality(BaseTestCommFunctionality):

    @pytest.fixture
    def comm_interface(self):
        return STM32_UART()