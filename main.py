from twisted.internet import protocol, reactor, endpoints, task
from twisted.internet.interfaces import IAddress

from src import Buffer
from src.packets import Packet
from src.player import Player
from src.stages import HandShake, Status, Login, Configuration, Play
from src.structs import VarInt


class State:
    HANDSHAKE = -1
    PLAY = 0
    STATUS = 1
    LOGIN = 2
    CONFIGURATION = 3


STATES = {
    State.HANDSHAKE: HandShake,
    State.PLAY: Play,
    State.STATUS: Status,
    State.LOGIN: Login,
    State.CONFIGURATION: Configuration,
}


class Server(protocol.Protocol):
    def __init__(self) -> None:
        self.player = Player(self)
        self.state = STATES[-1](self.player)
        self.keepalive_loop = task.LoopingCall(self.keepalive)

    def keepalive(self) -> None:
        keepalive = Packet(packet_id=0x24)
        keepalive.pack_long(1)
        self.send(keepalive)

    def dataReceived(self, data: bytes) -> None:
        buffer = Buffer(initial_bytes=data)
        next_state = self.state.process_packet(
            Packet(initial_bytes=buffer.read(buffer.unpack_varint()))
        )

        if next_state is not None:
            self.state = STATES[next_state](self.player)

        next_packet = buffer.read()
        if next_packet:
            self.dataReceived(next_packet)

    def send(self, packet: Packet) -> None:
        self.transport.write(VarInt.pack(len(packet.getvalue())) + packet.getvalue())


class ServerFactory(protocol.ServerFactory):
    def buildProtocol(self, addr: IAddress) -> protocol.Protocol | None:
        return Server()


endpoints.serverFromString(reactor, "tcp:25565").listen(ServerFactory())
reactor.run()
