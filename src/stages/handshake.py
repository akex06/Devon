from src.stages.stage import Stage, listen
from src.structs import (
    UShort,
    String,
    VarInt,
)


class HandShake(Stage):
    listeners = dict()
    packet_mapping = {0: [VarInt, String, UShort, VarInt]}

    @listen(0)
    def handshake(
        self, protocol_version: int, server_address: str, port: int, next_state: int
    ) -> int:
        print(f"{protocol_version=}")
        print(f"{server_address=}")
        print(f"{port=}")
        print(f"{next_state=}")
        return next_state
