import uuid

from src.packets.packet import Packet
from src.stages.stage import listen, Stage
from src.structs import String, UUID


class Login(Stage):
    packet_mapping = {0: [String, UUID], 3: []}
    listeners = dict()

    @listen(0)
    def status_request(self, name: str, _uuid: uuid.UUID) -> None:
        print(name, _uuid)

        login_success = Packet(packet_id=0x2)
        login_success.pack_uuid(_uuid)
        login_success.pack_string(name)
        login_success.pack_varint(0)

        self.player.send(login_success)

    @listen(3)
    def login_acknowledge(self) -> int:
        registry_data = Packet(packet_id=0x5)
        with open("registry_info.packet", "rb") as f:
            registry_data.write(f.read())

        self.player.send(registry_data)

        finish_config = Packet(packet_id=0x2)
        self.player.send(finish_config)

        return 3
