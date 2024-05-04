import abc
import struct
import uuid
from io import BytesIO
from typing import Any, ClassVar


class BaseStruct(metaclass=abc.ABCMeta):
    @classmethod
    @abc.abstractmethod
    def pack(cls, val: Any) -> bytes:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def unpack(cls, buffer: BytesIO) -> Any:
        raise NotImplementedError


class Struct(int, BaseStruct):
    fmt: ClassVar[str]

    @classmethod
    def pack(cls, val: int) -> bytes:
        return struct.pack(cls.fmt, val)

    @classmethod
    def unpack(cls, buffer: BytesIO) -> bool:
        return buffer.unpack(cls.fmt)


class Boolean(Struct):
    fmt = "?"


class Byte(Struct):
    fmt = "b"


class UByte(Struct):
    fmt = "B"


class Short(Struct):
    fmt = "h"


class UShort(Struct):
    fmt = ">h"


class Int(Struct):
    fmt = ">i"


class Long(Struct):
    fmt = ">q"


class Float(Struct):
    fmt = ">f"


class Double(Struct):
    fmt = ">d"


class String(str, BaseStruct):
    @classmethod
    def pack(cls, val: str) -> bytes:
        encoded_str = val.encode("utf-8")
        return VarInt.pack(len(encoded_str)) + encoded_str

    @classmethod
    def unpack(cls, buffer: BytesIO) -> str:
        str_length = VarInt.unpack(buffer)
        return buffer.read(str_length).decode("utf-8")


Identifier = String


class VarInt(int, BaseStruct):
    @classmethod
    def pack(cls, val: int) -> bytes:
        if val < 0:
            val = (1 << 32) + val

        total = b""
        while val >= 0x80:
            bits = val & 0x7F
            val >>= 7
            total += struct.pack("B", (0x80 | bits))

        bits = val & 0x7F
        total += struct.pack("B", bits)

        return total

    @classmethod
    def unpack(cls, buffer: BytesIO) -> int:
        total = 0
        shift = 0

        val = 0x80
        while val & 0x80:
            val = struct.unpack("B", buffer.read(1))[0]
            total |= (val & 0x7F) << shift
            shift += 7

        if total & (1 << 31):
            total = total - (1 << 32)

        return total


class Position(tuple, BaseStruct):
    @classmethod
    def pack(cls, position: tuple[int, int, int]) -> bytes:
        return Long.pack(
            ((position[0] & 0x3FFFFFF) << 38)
            | ((position[2] & 0x3FFFFFF) << 12)
            | (position[1] & 0xFFF)
        )

    @classmethod
    def unpack(cls, buffer: BytesIO) -> tuple[int, int, int]:
        encoded_position = Long.unpack(buffer)

        x = encoded_position >> 38
        y = encoded_position & 0xFFF
        z = (encoded_position >> 12) & 0x3FFFFFF

        if x >= 1 << 25:
            x -= 1 << 26

        if y >= 1 << 11:
            y -= 1 << 12

        if z >= 1 << 25:
            z -= 1 << 26

        return x, y, z


class UUID(uuid.UUID, BaseStruct):
    @classmethod
    def pack(cls, _uuid: uuid.UUID) -> bytes:
        return _uuid.bytes

    @classmethod
    def unpack(cls, buffer: BytesIO) -> str:
        return uuid.UUID(bytes=buffer.read(16)).hex
