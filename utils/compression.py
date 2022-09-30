import gzip
from dataclasses import dataclass
from typing import Annotated


@dataclass
class ValueRange:
    min: int = 0
    max: int = 9

    def __call__(self, value):
        if value < self.min or value > self.max:
            raise ValueError(f"Value must be between {self.min} and {self.max}")
        return value


def gzip_decompress(data: list[int]) -> str:
    return gzip.decompress(bytes(data)).decode('utf-8')


def compress_to_gzip(data: str, level: Annotated[int, ValueRange(0, 10)] = 6) -> list[int]:
    return list(gzip.compress(data.encode('utf-8'), compresslevel=level))
