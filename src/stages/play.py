from src.stages.stage import listen, Stage
from src.structs import Boolean, Double, Float, VarInt, Position, Byte


class Play(Stage):
    listeners = dict()

    @listen(0x17)
    def set_player_position(
        self, x: Double, y: Double, z: Double, on_ground: Boolean
    ) -> None:
        print(x, y, z, on_ground)

    @listen(0x18)
    def set_player_position_and_rotation(
        self,
        x: Double,
        y: Double,
        z: Double,
        yaw: Float,
        pitch: Float,
        on_ground: Boolean,
    ) -> None:
        print(x, y, z, yaw, pitch, on_ground)

    @listen(0x19)
    def set_player_rotation(self, yaw: Float, pitch: Float, on_ground: Boolean) -> None:
        print(yaw, pitch, on_ground)

    @listen(0x21)
    def player_action(
        self,
        status: VarInt,
        position: Position,
        face: Byte,
        sequence: VarInt,
    ) -> None:
        print(status, position, face, sequence)
