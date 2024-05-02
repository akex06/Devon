import json
from io import BytesIO

from twisted.internet import protocol, reactor, endpoints, task
from twisted.internet.interfaces import IAddress

from src import Buffer
from src.packets import Packet
from src.stages import stage
from src.structs import VarInt


class State:
    HANDSHAKE = -1
    PLAY = 0
    STATUS = 1
    LOGIN = 2
    CONFIGURATION = 3


STATES = {State.HANDSHAKE: stage.HandShake}


def get_status(
    *,
    max_players: int,
    player_amount: int,
    players: list[dict] = None,
    description: str,
):
    if players is None:
        players = list()

    return json.dumps(
        {
            "version": {"name": "1.20.4", "protocol": 765},
            "players": {"max": max_players, "online": player_amount, "sample": players},
            "description": {"text": description},
            "favicon": "data:image/png;base64,<data>",
            "enforcesSecureChat": True,
            "previewsChat": True,
        }
    )


class Server(protocol.Protocol):
    def __init__(self) -> None:
        self.state = STATES[-1]()
        self.keepalive_loop = task.LoopingCall(self.keepalive)

    def keepalive(self) -> None:
        keepalive = Packet(packet_id=0x24)
        keepalive.pack_long(1)
        self.send(keepalive)

    def dataReceived(self, data: bytes) -> None:
        buffer = Buffer(initial_bytes=data)
        print("-------------------------------")
        print("RECEIVED DATA")
        print(data.hex(" "))

        next_state = self.state.process_packet(
            Packet(initial_bytes=buffer.read(buffer.unpack_varint()))
        )

        if next_state is not None:
            self.state = STATES[next_state]()

        print("NEXT PACKET")
        next_packet = buffer.read()
        print(next_packet.hex(" "))
        if next_packet:
            self.dataReceived(next_packet)

    def send(self, packet: Packet) -> None:
        self.transport.write(VarInt.pack(len(packet.getvalue())) + packet.getvalue())


class ServerFactory(protocol.ServerFactory):
    def buildProtocol(self, addr: IAddress) -> protocol.Protocol | None:
        return Server()


endpoints.serverFromString(reactor, "tcp:25565").listen(ServerFactory())
reactor.run()
