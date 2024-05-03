from typing import Self

from twisted.internet.protocol import Protocol

from src.buffer import Buffer
from src.structs import VarInt


class Packet(Buffer):
    def __init__(self, *, packet_id: int = None, initial_bytes=b"") -> None:
        super().__init__(initial_bytes)

        if packet_id is None and initial_bytes is None:
            raise NotImplementedError("You need to pass packet_id or initial_bytes")

        if packet_id is None:
            self.id = self.unpack_varint()
        else:
            self.id = packet_id
            self.pack_varint(packet_id)

    def print(self) -> None:
        print(self.getvalue())
        print("".join([f"{x:02x} " for x in self.getvalue()]))
