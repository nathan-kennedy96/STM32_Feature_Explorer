
import logging
from serial import serial_for_url
from serial.serialutil import SerialException
from serial.tools.list_ports import comports

logging.basicConfig(level=logging.DEBUG)

INTERFACE_NAME = "STM32"
BAUD = 115200
HWID = "0403:6001"

class STM32ConnectionError(Exception):
    """Failed to Connect to the Adapter..."""

class STM32_UART:
    """Communicate with STM32 via UART.
    
    Uses the SH-U09C5 USB to TTL Adapter.
    https://www.deshide.com/product-details.html?pid=303205&_t=1661493660

    """

    def __init__(self, name: str = INTERFACE_NAME, hwid: str = HWID):
        self.logger = logging.getLogger(name)
        self.logger.info(f"Connecting to STM32 via hwid {hwid}")
        try:
            self.ser = serial_for_url(f"hwgrep://{hwid}", baudrate=BAUD)
        except SerialException:
            self.logger.error(f"Failed to find USB TTL Adapter....")
            self.logger.info("Only Found:")
            for port in comports():
                self.logger.info(f"\tDescription: {port.description}, HWID: {port.hwid}")
            raise STM32ConnectionError("Failed to Find the UART Adapter... Is HWID correct?")
        self.logger.info(f"Connection Successful")


    def read(self):
        ret = self.ser.readline().decode().strip()
        self.logger.debug(f"Received {ret}")


if __name__ == "__main__":
    stm32 = STM32_UART()
    while True:
        stm32.read()