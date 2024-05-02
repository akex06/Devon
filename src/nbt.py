import abc
import struct
from typing import Any, ClassVar

from src.buffer import Buffer

tag_ids = dict()


class Tag(metaclass=abc.ABCMeta):
    id: ClassVar[int] = None
    fmt: ClassVar[str | None] = None

    def __init__(self, name: str, value: Any) -> None:
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return self.tostring()

    def tostring(self, indent: int = 0) -> str:
        raise NotImplementedError

    def to_bytes(self) -> bytes:
        """Returns bytes representing the full tag with name and id"""
        return self.pack(self.id, self.get_value())

    @abc.abstractmethod
    def get_value(self) -> bytes:
        """Returns bytes representing just the value of the object, nameless and ID-less"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def from_buffer(cls, buffer: Buffer, *, named: bool = True):
        raise NotImplementedError

    @classmethod
    def from_bytes(cls, b: bytes):
        return cls.from_buffer(Buffer(b))

    @staticmethod
    def pack_string(text: str) -> bytes:
        data = text.encode("utf-8")
        return struct.pack(">H", len(data)) + data

    @staticmethod
    def unpack_string(buffer: Buffer) -> str:
        return buffer.read(buffer.unpack_ushort()).decode("utf-8")

    def pack(self, tag_id: int, tag_data: bytes) -> bytes:
        name = self.pack_string(self.name) if self.name is not None else b""
        return self.pack_id(tag_id) + name + tag_data

    @staticmethod
    def pack_id(tag_id: int) -> bytes:
        return struct.pack("b", tag_id)


class StructTag(Tag):
    def tostring(self, indent: int = 0) -> str:
        return (
            " " * indent
            + f"TAG_{type(self).__name__}({repr(self.name)}) {repr(self.value)}"
        )

    def get_value(self) -> bytes:
        return struct.pack(self.fmt, self.value)

    @classmethod
    def from_buffer(cls, buffer: Buffer, *, named: bool = True):
        name = buffer.read(buffer.unpack(">H")).decode("utf-8") if named else None
        return cls(name, buffer.unpack(cls.fmt))


class ArrayTag(Tag):
    def tostring(self, indent: int = 0) -> str:
        inner_tags = "\n".join([tag.tostring(indent + 2) for tag in self.value])

        gap = " " * indent
        return (
            gap
            + f"TAG_{type(self).__name__}({repr(self.name)}) {{\n{inner_tags}\n"
            + gap
            + "}"
        )

    def get_value(self) -> bytes:
        length = struct.pack(">i", len(self.value))
        array = b""

        for element in self.value:
            array += struct.pack(self.fmt, element.get_value())

        encoded_array = length + array
        return encoded_array

    @classmethod
    def from_buffer(cls, buffer: Buffer, *, named: bool = True):
        name = Tag.unpack_string(buffer) if named else None

        value = []
        for _ in range(buffer.unpack_int()):
            value.append(buffer.unpack(cls.fmt))

        return cls(name, value)


class Byte(StructTag):
    id = 1
    fmt = "b"


class Short(StructTag):
    id = 2
    fmt = ">h"


class Int(StructTag):
    id = 3
    fmt = ">i"


class Long(StructTag):
    id = 4
    fmt = ">q"


class Float(StructTag):
    id = 5
    fmt = ">f"


class Double(StructTag):
    id = 6
    fmt = ">d"


class ByteArray(ArrayTag):
    id = 7
    fmt = "b"


class String(ArrayTag):
    id = 8

    def tostring(self, indent: int = 0) -> str:
        return (
            " " * indent
            + f"TAG_{type(self).__name__}({repr(self.name)}) {repr(self.value)}"
        )

    def get_value(self) -> bytes:
        return self.pack_string(self.value)

    @classmethod
    def from_buffer(cls, buffer: Buffer, *, named: bool = True):
        return cls(
            Tag.unpack_string(buffer) if named else None, Tag.unpack_string(buffer)
        )


class List(ArrayTag):
    id = 9
    value: list[Tag]

    def __init__(self, _type: int, name: str, value: Any):
        self.type = _type
        super().__init__(name, value)

    def get_value(self) -> bytes:
        encoded_list = self.pack_id(self.type)
        encoded_list += struct.pack(">I", len(self.value))
        for element in self.value:
            encoded_list += element.get_value()

        return encoded_list

    @classmethod
    def from_buffer(cls, buffer: Buffer, *, named: bool = True):
        name = Tag.unpack_string(buffer) if named else None
        tag_id = buffer.unpack_byte()
        length = buffer.unpack_int()

        elements = list()
        for _ in range(length):
            tag = tag_ids[tag_id]

            element = tag.from_buffer(buffer, named=False)
            elements.append(element)

        return cls(tag_id, name, elements)


class Compound(ArrayTag):
    id = 10
    value: list[Tag]

    def get_value(self) -> bytes:
        compound = b""
        for element in self.value:
            compound += element.to_bytes()

        return compound + b"\x00"

    @classmethod
    def from_bytes(cls, b: bytes, named: bool = True, root_tag: bool = False):
        return cls.from_buffer(Buffer(b), named=named, root_tag=root_tag)

    @classmethod
    def from_buffer(cls, buffer: Buffer, *, named: bool = True, root_tag: bool = False):
        if root_tag:
            buffer.unpack_byte()

        name = Tag.unpack_string(buffer) if named else None
        value = list()
        while True:
            tag_id = buffer.unpack_byte()
            if tag_id == 0:
                break

            tag = tag_ids[tag_id].from_buffer(buffer)
            value.append(tag)

        return cls(name, value)


class IntArray(ArrayTag):
    id = 11
    fmt = ">i"


class LongArray(ArrayTag):
    id = 12
    fmt = ">q"


tag_ids.update(
    {
        1: Byte,
        2: Short,
        3: Int,
        4: Long,
        5: Float,
        6: Double,
        7: ByteArray,
        8: String,
        9: List,
        10: Compound,
        11: IntArray,
        12: LongArray,
    }
)
