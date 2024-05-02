from src.buffer import Buffer


class Packet(Buffer):
    def __init__(self, *, packet_id: int = None, initial_bytes=b"") -> None:
        super().__init__(initial_bytes)

        if packet_id is None and initial_bytes is None:
            raise NotImplementedError("You need to pass packet_id or initial_bytes")

        if packet_id is None:
            self.id = self.unpack_varint()
        else:
            self.id = packet_id

    def print(self) -> None:
        print(self.getvalue())
        print("".join([f"{x:02x} " for x in self.getvalue()]))
