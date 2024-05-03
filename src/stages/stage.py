import abc
from dataclasses import dataclass
from typing import Callable, ClassVar, Any

from src import structs
from src.packets.packet import Packet
from src.player import Player


class Stage(metaclass=abc.ABCMeta):
    packet_mapping: ClassVar[dict[int, list[structs.BaseStruct]]]
    listeners: list

    def __init__(self, player: Player) -> None:
        self.player = player

    @staticmethod
    def decode_args(packet, parameter_types) -> list[Any]:
        args = list()
        for parameter_type in parameter_types:
            args.append(parameter_type.unpack(packet))

        return args

    def process_packet(self, packet: Packet) -> int | None:
        print("------------------------------------------------")
        print(f"Raw Data: {packet.getvalue().hex(' ')}")
        print(f"State: {type(self).__name__}")
        print(f"Packet ID: {hex(packet.id)}")

        if packet.id not in self.packet_mapping:
            print("PACKET NOT IMPLEMENTED")
            return

        func, parameter_types = self.listeners[packet.id]
        parameters = self.decode_args(packet, parameter_types)
        return func(self, *parameters)


@dataclass
class listen_wrap:
    packet_id: int
    fn: Callable
    owner: Stage = None

    def __set_name__(self, owner, name):
        self.owner = owner
        self.owner.listeners[self.packet_id] = (
            self.fn,
            self.owner.packet_mapping[self.packet_id],
        )

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


def listen(packet_id: int):
    return lambda func: listen_wrap(packet_id, func)
