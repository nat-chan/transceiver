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
        # 現在のプロセスで管理されているname
        self.current_process_managed_name: set[str] = set()

    @staticmethod
    def pre(name: str) -> str:
        """管理を容易にするために共通するprefixを付ける"""
        return f"transceiver-{name}"

    def is_exists(self, name: str) -> bool:
        """
        nameで指定されたshared memoryが存在するか判定
        """
        try:
            shared_memory.SharedMemory(name=self.pre(name))
            return True
        except FileNotFoundError:
            return False

    def release(self, name: str):
        """
        nameで指定されたshared memoryを解放する
        """
        shm = shared_memory.SharedMemory(name=self.pre(name))
        shm.close()
        shm.unlink()
        self.current_process_managed_name.remove(self.pre(name))

    def read_numpy(self, name: str) -> np.ndarray:
        """
        shared memoryからnumpy arrayを読み込む
        メモリ上で共有されたnumpy arrayを作成して返す
        """
        assert self.is_exists(name), f"{name} is not exists"
        try:
            shm = shared_memory.SharedMemory(name=self.pre(name))
        except FileNotFoundError as err:
            raise RuntimeError(f"{name}が存在していません") from err

        serialized_data_field_nbytes = shm.buf[-utils.offset_nbytes :]
        data_field_nbytes = utils.length_from_bytes(serialized_data_field_nbytes)
        data_field = utils.data_field_from_buffer(
            shm.buf[-(data_field_nbytes + utils.offset_nbytes) : -utils.offset_nbytes]
        )
        data_format = data_field["data_format"]
        dtype = data_field["dtype"]
        shape = data_field["shape"]
        assert (
            data_format == "numpy"
        ), f"この関数では{data_format}はサポートされていません"

        shared_array = np.ndarray(
            shape,
            dtype=dtype,
            buffer=shm.buf[: -(data_field_nbytes + utils.offset_nbytes)],
        )
        return shared_array

    def write_numpy(self, name: str, array: np.ndarray) -> np.ndarray:
        """
        shared memoryにnumpy arrayを書き込む
        メモリ上で共有されたnumpy arrayを作成して返す
        共有されたarrayのshapeやdtypeの変更などは即時には反映されない
        """
        data_field = {
            "data_format": "numpy",
            "shape": array.shape,
            "dtype": utils.dtype_to_str(array),
        }
        serialized_data_field = utils.data_field_to_bytes(data_field)
        data_field_nbytes = len(serialized_data_field)
        serialized_data_field_nbytes = utils.length_to_bytes(data_field_nbytes)
        assert len(serialized_data_field_nbytes) == utils.offset_nbytes

        # TODO: nameが既に存在しているときの処理
        shm = shared_memory.SharedMemory(
            create=True,
            size=array.nbytes + data_field_nbytes + utils.offset_nbytes,
            name=self.pre(name),
        )

        # write numpy buffer
        shared_array = np.ndarray(
            array.shape,
            dtype=array.dtype,
            buffer=shm.buf[: -(data_field_nbytes + utils.offset_nbytes)],
        )
        np.copyto(shared_array, array)

        # write data field
        shm.buf[-(data_field_nbytes + utils.offset_nbytes) : -utils.offset_nbytes] = (
            serialized_data_field
        )

        # write offset
        shm.buf[-utils.offset_nbytes :] = serialized_data_field_nbytes

        self.current_process_managed_name.add(self.pre(name))

        return shared_array

    def list_managed_name(self) -> list[str]:
        """
        現在のプロセスで管理されているshared memory nameの一覧
        """
        results = [
            name.removeprefix("transceiver-")
            for name in self.current_process_managed_name
        ]
        return results

    def list_all_name(self) -> list[str]:
        """
        複数のプロセスがこのライブラリを使うことを想定していて
        self.current_process_managed_name で管理されていないshared memory
        が存在する場合があるので/dev/shmを検索して
        transceiverが扱うことのできるshared memory nameの一覧を返す
        """
        results = [
            filepath.name.removeprefix("transceiver-")
            for filepath in Path("/dev/shm").glob("transceiver-*")
        ]
        return results


transceiver = Transceiver()
