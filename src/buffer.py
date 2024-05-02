import inspect
import io
import struct
from typing import Any

from src import structs


class Buffer(io.BytesIO):
    def pack(self, fmt: str, value: Any):
        self.write(struct.pack(fmt, value))

    def unpack(self, fmt: str) -> Any:
        return struct.unpack(fmt, self.read(struct.calcsize(fmt)))[0]

    def pack_bool(self, val: bool) -> None:
        self.write(structs.Boolean.pack(val))

    def unpack_bool(self) -> bool:
        return structs.Boolean.unpack(self)

    def pack_byte(self, val: int) -> None:
        self.write(structs.Byte.pack(val))

    def unpack_byte(self) -> int:
        return structs.Byte.unpack(self)

    def pack_ubyte(self, val: int) -> None:
        self.write(structs.UByte.pack(val))

    def unpack_ubyte(self) -> int:
        return structs.UByte.unpack(self)

    def pack_short(self, val: int) -> None:
        self.write(structs.Short.pack(val))

    def unpack_short(self) -> int:
        return structs.Short.unpack(self)

    def pack_ushort(self, val: int) -> None:
        self.write(structs.UShort.pack(val))

    def unpack_ushort(self) -> int:
        return structs.UShort.unpack(self)

    def pack_int(self, val: int) -> None:
        self.write(structs.Int.pack(val))

    def unpack_int(self) -> int:
        return structs.Int.unpack(self)

    def pack_long(self, val: int) -> None:
        self.write(structs.Long.pack(val))

    def unpack_long(self) -> int:
        return structs.Long.unpack(self)

    def pack_float(self, val: int) -> None:
        self.write(structs.Float.pack(val))

    def unpack_float(self) -> int:
        return structs.Float.unpack(self)

    def pack_double(self, val: int) -> None:
        self.write(structs.Double.pack(val))

    def unpack_double(self) -> int:
        return structs.Double.unpack(self)

    def pack_string(self, val: str) -> None:
        self.write(structs.String.pack(val))

    def unpack_string(self) -> str:
        return structs.String.unpack(self)

    def pack_varint(self, val: int) -> None:
        self.write(structs.VarInt.pack(val))

    def unpack_varint(self) -> int:
        return structs.VarInt.unpack(self)

    def pack_position(self, x: int, y: int, z: int) -> None:
        self.write(structs.Position.pack((x, y, z)))

    def unpack_position(self) -> tuple[int, int, int]:
        return structs.Position.unpack(self)
