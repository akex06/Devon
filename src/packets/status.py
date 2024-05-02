from src.packets import Packet


class StatusResponse(Packet):
    def __init__(self, status: dict):
        super().__init__(packet_id=0x00)
        self.status = status



