import abc
import inspect
from typing import Callable, Any

from src.packets.packet import Packet
from src.player import Player


class Stage(metaclass=abc.ABCMeta):
    listeners: list[int, Callable]

    def __init__(self, player: Player) -> None:
        self.player = player

    @staticmethod
    def decode_args(func: Callable, packet: Packet) -> list[Any]:
        args = list()
        parameter_types = inspect.signature(func).parameters.values()

        for parameter_type in parameter_types:
            if parameter_type.name == "self":
                continue

            struct = parameter_type.annotation
            args.append(struct(struct.unpack(packet)))

        return args

    def process_packet(self, packet: Packet) -> int | None:
        print("------------------------------------------------")
        print(f"Raw Data: {packet.getvalue().hex(' ')}")
        print(f"State: {type(self).__name__}")
        print(f"Packet ID: {hex(packet.id)}")

        if packet.id not in self.listeners:
            print("PACKET NOT IMPLEMENTED")
            return

        func = self.listeners[packet.id]
        parameters = self.decode_args(func, packet)
        return func(self, *parameters)


class listen_wrap:
    def __init__(self, packet_id: int, fn: Callable, owner: Stage = None) -> None:
        self.packet_id = packet_id
        self.fn = fn
        self.owner = owner

    def __set_name__(self, owner, name):
        self.owner = owner
        self.owner.listeners[self.packet_id] = self.fn

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


def listen(packet_id: int):
    return lambda func: listen_wrap(packet_id, func)
