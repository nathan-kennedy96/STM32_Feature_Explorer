from python.command import Command
from numpy import dtype, uint8, uint16, uint32
from typing import Dict

CMD_TO_DTYPE: Dict[Command, dtype] = {
    Command.HELLO: uint16,
    Command.NOK: uint8,
    Command.TIME: uint32,
}
