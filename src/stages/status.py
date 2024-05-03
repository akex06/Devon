import json

from src.packets.packet import Packet
from src.stages.stage import listen, Stage
from src.structs import Long


class Status(Stage):
    packet_mapping = {0: (), 1: [Long]}
    listeners = dict()

    @staticmethod
    def get_status(
        max_players: int,
        player_amount: int,
        players: list[dict] = None,
        description: str = "",
    ):
        if players is None:
            players = list()

        return json.dumps(
            {
                "version": {"name": "1.20.4", "protocol": 765},
                "players": {
                    "max": max_players,
                    "online": player_amount,
                    "sample": players,
                },
                "description": {"text": description},
                "favicon": "data:image/png;base64,<data>",
                "enforcesSecureChat": True,
                "previewsChat": True,
            }
        )

    @listen(0)
    def status_request(self) -> None:
        status = Packet(packet_id=0x00)
        status.pack_string(
            self.get_status(
                max_players=69,
                player_amount=3,
                players=None,
                description="Puto el que lo lea",
            )
        )
        print(status.getvalue())
        self.player.send(status)

    @listen(1)
    def ping_request(self, value: int) -> None:
        ping = Packet(packet_id=0x01)
        ping.pack_long(value)
        self.player.send(ping)
