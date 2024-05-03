from src.stages.stage import listen, Stage
from src.structs import Boolean, Double, Float, VarInt, Position, Byte


class Play(Stage):
    packet_mapping = {
        0x17: [Double, Double, Double, Boolean],
        0x18: [Double, Double, Double, Float, Float, Boolean],
        0x19: [Float, Float, Boolean],
        0x21: [VarInt, Position, Byte, VarInt],
    }
    listeners = dict()

    @listen(0x17)
    def set_player_position(self, x: int, y: int, z: int, on_ground: bool) -> None:
        print(x, y, z, on_ground)

    @listen(0x18)
    def set_player_position_and_rotation(
        self, x: int, y: int, z: int, yaw: float, pitch: float, on_ground: bool
    ) -> None:
        print(x, y, z, yaw, pitch, on_ground)

    @listen(0x19)
    def set_player_rotation(self, yaw: float, pitch: float, on_ground: bool) -> None:
        print(yaw, pitch, on_ground)

    @listen(0x21)
    def player_action(
        self, status: int, position: tuple[int, int, int], face: int, sequence: int
    ) -> None:
        print(status, position, face, sequence)
