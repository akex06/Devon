import io
import struct
import uuid
from typing import Any

from src.structs import (
    UUID,
    Boolean,
    Byte,
    UByte,
    Short,
    UShort,
    String,
    Int,
    Long,
    Double,
    VarInt,
    Position,
    Float,
)


class Buffer(io.BytesIO):
    def pack(self, fmt: str, value: Any):
        self.write(struct.pack(fmt, value))

    def unpack(self, fmt: str) -> Any:
        return struct.unpack(fmt, self.read(struct.calcsize(fmt)))[0]

    def pack_bool(self, val: bool) -> None:
        self.write(Boolean.pack(val))

    def unpack_bool(self) -> bool:
        return Boolean.unpack(self)

    def pack_byte(self, val: int) -> None:
        self.write(Byte.pack(val))

    def unpack_byte(self) -> int:
        return Byte.unpack(self)

    def pack_ubyte(self, val: int) -> None:
        self.write(UByte.pack(val))

    def unpack_ubyte(self) -> int:
        return UByte.unpack(self)

    def pack_short(self, val: int) -> None:
        self.write(Short.pack(val))

    def unpack_short(self) -> int:
        return Short.unpack(self)

    def pack_ushort(self, val: int) -> None:
        self.write(UShort.pack(val))

    def unpack_ushort(self) -> int:
        return UShort.unpack(self)

    def pack_int(self, val: int) -> None:
        self.write(Int.pack(val))

    def unpack_int(self) -> int:
        return Int.unpack(self)

    def pack_long(self, val: int) -> None:
        self.write(Long.pack(val))

    def unpack_long(self) -> int:
        return Long.unpack(self)

    def pack_float(self, val: int) -> None:
        self.write(Float.pack(val))

    def unpack_float(self) -> int:
        return Float.unpack(self)

    def pack_double(self, val: int) -> None:
        self.write(Double.pack(val))

    def unpack_double(self) -> int:
        return Double.unpack(self)

    def pack_string(self, val: str) -> None:
        self.write(String.pack(val))

    def unpack_string(self) -> str:
        return String.unpack(self)

    def pack_varint(self, val: int) -> None:
        self.write(VarInt.pack(val))

    def unpack_varint(self) -> int:
        return VarInt.unpack(self)

    def pack_position(self, x: int, y: int, z: int) -> None:
        self.write(Position.pack((x, y, z)))

    def unpack_position(self) -> tuple[int, int, int]:
        return Position.unpack(self)

    def pack_uuid(self, _uuid: uuid.UUID) -> None:
        self.write(UUID.pack(_uuid))

    def unpack_uuid(self) -> uuid.UUID:
        return UUID.unpack(self)
