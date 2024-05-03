from twisted.internet import task
from twisted.internet.protocol import Protocol

from src import nbt
from src.buffer import Buffer
from src.packets.packet import Packet
from src.player import Player
from src.stages.stage import listen, Stage


class Configuration(Stage):
    packet_mapping = {0: []}
    listeners = dict()

    def __init__(self, player: Player):
        super().__init__(player)

        self.keep_alive_loop = task.LoopingCall(self.keep_alive)

    def keep_alive(self) -> None:
        keep_alive = Packet(packet_id=0x24)
        keep_alive.pack_long(1)

        self.player.send(keep_alive)

    @listen(0)
    def ack_finish_config(self) -> int:
        self.keep_alive_loop.start(15.0)

        login_play = Packet(packet_id=0x29)
        login_play.pack_int(0)
        login_play.pack_bool(False)
        login_play.pack_varint(4)
        login_play.pack_string("minecraft:overworld")
        login_play.pack_string("minecraft:overworld_caves")
        login_play.pack_string("minecraft:the_nether")
        login_play.pack_string("minecraft:the_end")
        login_play.pack_varint(20)
        login_play.pack_varint(10)
        login_play.pack_varint(8)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_string("minecraft:overworld")
        login_play.pack_string("overworld")
        login_play.pack_long(0)
        login_play.pack_ubyte(1)
        login_play.pack_byte(-1)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_bool(False)
        login_play.pack_varint(0)

        self.player.send(login_play)

        game_event = Packet(packet_id=0x20)
        game_event.pack_ubyte(13)
        game_event.pack_float(0)

        self.player.send(game_event)

        chunk_data = Packet(packet_id=0x25)
        chunk_data.pack_int(0)
        chunk_data.pack_int(0)

        chunk_data.write(nbt.Compound(None, []).to_bytes())

        chunk = Buffer()

        # chunk section
        for _ in range(24):
            chunk.pack_short(16**3)

            # block palette
            chunk.pack_ubyte(0)
            chunk.pack_varint(17)
            chunk.pack_varint(0)

            # chunk palette
            chunk.pack_ubyte(0)
            chunk.pack_varint(0)
            chunk.pack_varint(0)

        chunk_data.pack_varint(len(chunk.getvalue()))
        chunk_data.write(chunk.getvalue())

        chunk_data.pack_varint(0)

        chunk_data.pack_byte(0)
        chunk_data.pack_byte(0)
        chunk_data.pack_byte(0)
        chunk_data.pack_byte(0)

        chunk_data.pack_varint(0)
        chunk_data.pack_varint(0)
        chunk_data.print()

        self.player.send(chunk_data)

        return 0
