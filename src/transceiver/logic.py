from multiprocessing import shared_memory
from pathlib import Path
from typing import Literal

import numpy as np

from transceiver import utils

__doc__ = """shmのデータアライメント
┃                 numpy array buffer              ┃   literal data field   ┃ offset  ┃
┠────┼────┼────┼────┼────┼────┼────┼────┼────┼────╂────┼────┼────┼────┼────╂────┼────┨
┃    │    │    │    │    │    │    │    │    │    ┃    │    │    │    │    ┃    │    ┃
┠────┼────┼────┼────┼────┼────┼────┼────┼────┼────╂────┼────┼────┼────┼────╂────┼────┨
┃                 numpy array nbytes              ┃    offset - 2 bytes    ┃ 2 bytes ┃
""".strip()


data_format_t = Literal[
    "numpy",
    "pytorch",
    "PIL",
]
data_format_list = data_format_t.__args__


class Transceiver:
    def __init__(self):
        pass

    @staticmethod
    def pre(name: str) -> str:
        """管理を容易にするために共通するprefixを付ける"""
        return f"transceiver-{name}"

    def read_numpy(self, name: str) -> np.ndarray:
        name = self.pre(name)
        # TODO: nameが存在しなかったときの処理
        shm = shared_memory.SharedMemory(name=name)
        pass

    def write(self, name: str, data_format: data_format_t):
        name = self.pre(name)
        pass

    def write_numpy(self, name: str, array: np.ndarray):
        name = self.pre(name)
        data_field = {
            "data_format": "numpy",
            "shape": array.shape,
            "dtype": utils.dtype_to_str(array),
        }
        serialized = utils.serialize_data_field(data_field)
        pass

    def list_managed_name(self) -> list[str]:
        results = [
            filepath.name.removeprefix("transceiver-")
            for filepath in Path("/dev/shm").glob("transceiver-*")
        ]
        return results


def test_Transceiver():
    transceiver = Transceiver()
    array = np.zeros((10, 10), dtype=np.uint8)
    transceiver.write_numpy("test", array)


if __name__ == "__main__":
    test_Transceiver()
