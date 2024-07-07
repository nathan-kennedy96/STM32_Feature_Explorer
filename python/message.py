import numpy as np
from command import Command

class Message: 
    #TODO: can this dtype be inferred from the struct/c code?
    dtype: np.dtype =  np.dtype([
    ("command", np.int16),
    ("data", np.uint16),
    ]) 

    def __init__(self, cmd: Command = None, data: int = None):
        if cmd is None:
            self._ar = np.array([], dtype=self.dtype)
        else:
            self._ar = np.array([(cmd.value,data)], dtype=self.dtype)


    
    @classmethod
    def load(cls, data: bytes):
        msg = cls(None, None)
        msg._ar = np.frombuffer(data, dtype=Message.dtype)
        return msg 
    @property
    def command(self):
        return self._ar["command"]

    @property
    def data(self):
        return self._ar["data"]
    
    def __str__(self):
        return f"Command: {self.command}\t Data: {self.data}"

    def __bytes__(self):
        return bytes(self._ar)