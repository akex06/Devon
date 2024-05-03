from twisted.internet.protocol import Protocol

from src.packets.packet import Packet
from src.structs import VarInt


class Player:
    def __init__(self, protocol: Protocol) -> None:
        self.protocol = protocol
        self.pos = 0, 90, 0

    def send(self, packet: Packet) -> None:
        # noinspection PyArgumentList
        self.protocol.transport.write(
            VarInt.pack(len(packet.getvalue())) + packet.getvalue()
        )
