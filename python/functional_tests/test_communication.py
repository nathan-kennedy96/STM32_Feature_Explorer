import pytest
from time import sleep
from datetime import datetime, timedelta, timezone
import logging
from python.comm_base import STM32_COM_BASE
from python.message import Message
from python.command import Command
from python.eth_comm import STM32_TCP
from python.uart_comm import STM32_UART


class BaseTestCommFunctionality:

    @pytest.fixture(autouse=True)
    def setup_teardown(self, comm_interface: STM32_COM_BASE):
        self.comm = comm_interface
        yield
        self.comm.teardown()

    @pytest.mark.parametrize(
        "data_number, expected_response",
        [
            # Hello is programmed to respond with data incremented by one
            ([1234], [1235]),
            ([0], [1]),
            ([999], [1000]),
        ],
    )
    def test_hello_message(self, data_number, expected_response):
        """Test that the hello message returns a response with correct Command and data"""
        hello_msg = Message(Command.HELLO, [data_number])
        response_message = self.comm.exchange(hello_msg)
        assert response_message.data == expected_response

    @pytest.mark.parametrize(
        "command, data, expected_command, expected_data",
        [(Command.NOK, [0], Command.NOK, [0]), (Command.NOK, [123], Command.NOK, [0])],
    )
    def test_nok_message(self, command, data, expected_command, expected_data):
        """Test that the NOK message or unknown message responds with the expected NOK message."""
        nok_msg = Message(command, data)
        response_message = self.comm.exchange(nok_msg)
        assert response_message.data == expected_data
        assert response_message.command == expected_command
        assert response_message == Message(expected_command, expected_data)

    def test_time_usage(self):
        """Test that we can set and get time"""
        # TODO: Once we implement timestamps with higher resolution than 1s -> reduce these sleeps.
        # Capture the current time in UTC, rounded to the nearest second
        now = datetime.now(timezone.utc).replace(microsecond=0)

        # Set the time on the STM32 and get the response
        response_time = self.comm.set_time(now)

        # Assert that the response time matches the set time exactly (since STM32 has no microseconds)
        assert response_time == now, f"Expected {now}, but got {response_time}"

        # Sleep for 2.1 seconds gives some buffer to RTC
        sleep(2.1)

        # Get the time from the STM32 after sleeping
        second_time = self.comm.get_time()

        # Assert that the time has advanced by at least 2 seconds
        assert second_time - now >= timedelta(
            seconds=2
        ), f"Expected at least 2 seconds difference, but got {second_time - now}"


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
