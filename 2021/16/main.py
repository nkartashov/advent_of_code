from typing import List, NamedTuple, Tuple, Union, Any
from enum import Enum
import math
import functools
import operator


def assrt(want, f, *args, **kwargs):
    got = f(*args, **kwargs)
    if got != want:
        print(f"{f.__qualname__} returned {got}, expected {want}")


class Type(Enum):
    SUM = 0b000
    PRODUCT = 0b001
    MIN = 0b010
    MAX = 0b011
    LITERAL = 0b100
    GT = 0b101
    LT = 0b110
    EQ = 0b111


class Literal(NamedTuple):
    version: int
    value: int

    def eval(self):
        return self.value


class Operator(NamedTuple):
    version: int
    op_type: Type
    subpackets: List[Union[Literal, "Operator"]]

    def eval(self) -> int:
        if self.op_type == Type.SUM:
            return sum(op.eval() for op in self.subpackets)

        if self.op_type == Type.PRODUCT:
            return math.prod(op.eval() for op in self.subpackets)

        if self.op_type == Type.MIN:
            return min(op.eval() for op in self.subpackets)

        if self.op_type == Type.MAX:
            return max(op.eval() for op in self.subpackets)

        assert len(self.subpackets) == 2

        a, b = (op.eval() for op in self.subpackets)
        if self.op_type == Type.GT:
            return 1 if a > b else 0

        if self.op_type == Type.LT:
            return 1 if a < b else 0

        if self.op_type == Type.EQ:
            return 1 if a == b else 0

        raise RuntimeError("Unknown op type")


def bitstream_to_number(bitstream: List[str]) -> int:
    result = 0
    for x in bitstream:
        result = result * 2 + int(x)
    return result


assrt(4, bitstream_to_number, ["1", "0", "0"])
assrt(6, bitstream_to_number, ["1", "1", "0"])


def flatten(a: List[List[Any]]) -> List[Any]:
    return functools.reduce(operator.iconcat, a, [])


def hexstring_to_bitstream(hex: str) -> List[str]:
    return flatten([list(f"{int(ch, base=16):04b}") for ch in hex])


assrt(list("0110"), hexstring_to_bitstream, "6")
assrt(list("01100110"), hexstring_to_bitstream, "66")


assrt(list("110100101111111000101000"), hexstring_to_bitstream, "D2FE28")


def read_bits(bits: List[str], start, size) -> Tuple[int, int]:
    value = bitstream_to_number(bits[start : start + size])
    return value, start + size


LITERAL_CHUNK_SIZE = 5


def read_literal_value(bits: List[str], start) -> Tuple[int, int]:
    chunks = [bits[start : start + LITERAL_CHUNK_SIZE]]
    start += LITERAL_CHUNK_SIZE
    # last chunk has 1 as leading bit
    while chunks[-1][0] == "1":
        chunks.append(bits[start : start + LITERAL_CHUNK_SIZE])
        start += LITERAL_CHUNK_SIZE

    return bitstream_to_number(flatten([chunk[1:] for chunk in chunks])), start


TEST_LITERAL_BITS = list("110100101111111000101000")

assrt((2021, 21), read_literal_value, TEST_LITERAL_BITS, 6)


class SubpacketType(Enum):
    LENGTH = 0
    COUNT = 1


VERSION_SIZE = 3
TYPE_SIZE = 3
SUBPACKET_TYPE_SIZE = 1
SUBPACKET_LENGTH_SIZE = 15
SUBPACKET_COUNT_SIZE = 11


def parse(bits: List[str], start=0) -> Tuple[Any, int]:
    version, start = read_bits(bits, start, VERSION_SIZE)
    packet_type_value, start = read_bits(bits, start, TYPE_SIZE)
    packet_type = Type(packet_type_value)
    if packet_type == Type.LITERAL:
        value, start = read_literal_value(bits, start)
        return Literal(version=version, value=value), start

    subpacket_type_value, start = read_bits(bits, start, SUBPACKET_TYPE_SIZE)
    subpacket_type = SubpacketType(subpacket_type_value)
    subpackets = []
    new_start = -1
    if subpacket_type == SubpacketType.LENGTH:
        subpacket_length, start = read_bits(bits, start, SUBPACKET_LENGTH_SIZE)
        new_start = start + subpacket_length
        while start < new_start:
            subpacket, start = parse(bits, start)
            subpackets.append(subpacket)

    elif subpacket_type == SubpacketType.COUNT:
        subpacket_count, start = read_bits(bits, start, SUBPACKET_COUNT_SIZE)
        for _ in range(subpacket_count):
            subpacket, start = parse(bits, start)
            subpackets.append(subpacket)
        new_start = start

    else:
        assert False

    assert new_start != -1
    return (
        Operator(version=version, op_type=packet_type, subpackets=subpackets),
        new_start,
    )


TEST_RESULT_LITERAL = Literal(version=6, value=2021)

assrt((TEST_RESULT_LITERAL, 21), parse, TEST_LITERAL_BITS)

TEST_OPERATOR_TYPE0_BITS = list(
    "00111000000000000110111101000101001010010001001000000000"
)
TEST_OPERATOR_TYPE0_RESULT = Operator(
    version=1,
    op_type=Type.LT,
    subpackets=[
        Literal(version=6, value=10),
        Literal(version=2, value=20),
    ],
)
assrt((TEST_OPERATOR_TYPE0_RESULT, 49), parse, TEST_OPERATOR_TYPE0_BITS)

TEST_OPERATOR_TYPE1_BITS = list(
    "11101110000000001101010000001100100000100011000001100000"
)
TEST_OPERATOR_TYPE1_RESULT = Operator(
    version=7,
    op_type=Type.MAX,
    subpackets=[
        Literal(version=2, value=1),
        Literal(version=4, value=2),
        Literal(version=1, value=3),
    ],
)
assrt((TEST_OPERATOR_TYPE1_RESULT, 51), parse, TEST_OPERATOR_TYPE1_BITS)


def solve1(hex: str) -> int:
    bits = hexstring_to_bitstream(hex)
    result, _ = parse(bits)

    def recurse(op):
        if isinstance(op, Literal):
            return op.version

        assert isinstance(op, Operator)
        return op.version + sum(recurse(subop) for subop in op.subpackets)

    return recurse(result)


TEST_HEX1 = "8A004A801A8002F478"
TEST_HEX2 = "620080001611562C8802118E34"
TEST_HEX3 = "C0015000016115A2E0802F182340"
TEST_HEX4 = "A0016C880162017C3686B18A3D4780"

assrt(16, solve1, TEST_HEX1)
assrt(12, solve1, TEST_HEX2)
assrt(23, solve1, TEST_HEX3)
assrt(31, solve1, TEST_HEX4)


def solve2(hex: str) -> int:
    bits = hexstring_to_bitstream(hex)
    result, _ = parse(bits)
    return result.eval()


TEST_HEX5 = "C200B40A82"
TEST_HEX6 = "04005AC33890"
TEST_HEX7 = "880086C3E88112"
TEST_HEX8 = "CE00C43D881120"
TEST_HEX9 = "D8005AC2A8F0"
TEST_HEX10 = "F600BC2D8F"
TEST_HEX11 = "9C005AC2F8F0"
TEST_HEX12 = "9C0141080250320F1802104A08"

assrt(3, solve2, TEST_HEX5)
assrt(54, solve2, TEST_HEX6)
assrt(7, solve2, TEST_HEX7)
assrt(9, solve2, TEST_HEX8)
assrt(1, solve2, TEST_HEX9)
assrt(0, solve2, TEST_HEX10)
assrt(0, solve2, TEST_HEX11)
assrt(1, solve2, TEST_HEX12)


def main():
    with open("in.txt") as infile:
        hex_str = infile.readline().strip()
        print(solve1(hex_str))
        print(solve2(hex_str))


if __name__ == "__main__":
    main()
