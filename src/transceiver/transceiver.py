from multiprocessing import shared_memory  # noqa
import ast  # noqa
import numpy as np
from pathlib import Path
from typing import Literal


"""shmのデータアライメント
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

    def pre(name: str) -> str:
        """管理を容易にするために共通するprefixを付ける"""
        return f"transceiver-{name}"

    def read(self, name: str) -> np.ndarray:
        name = self.pre(name)
        pass

    def write(self, name: str, data_format: data_format_t):
        name = self.pre(name)
        pass

    def write_numpy(self, name: str, array: np.ndarray):
        name = self.pre(name)
        pass

    def list_managed_name(self) -> list[str]:
        results = [
            filepath.name.removeprefix("transceiver-")
            for filepath in Path("/dev/shm").glob("transceiver-*")
        ]
        return results
