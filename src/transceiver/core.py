from multiprocessing import shared_memory
from typing import Literal

import numpy as np

from transceiver import utils

__doc__ = """shmのデータアライメント
┃                 numpy array buffer              ┃   literal data field   ┃ offset  ┃
┠────┼────┼────┼────┼────┼────┼────┼────┼────┼────╂────┼────┼────┼────┼────╂────┼────┨
┃    │    │    │    │    │    │    │    │    │    ┃    │    │    │    │    ┃    │    ┃
┠────┼────┼────┼────┼────┼────┼────┼────┼────┼────╂────┼────┼────┼────┼────╂────┼────┨
┃                 numpy array nbytes              ┃    offset - 2 bytes    ┃ 2 bytes ┃

TODO:
- 大きいchannelにはより小さいデータを流せるようにする
- writeを以下の二つに分ける
    - create channel
    - send to channel
- readを以下に変更
    - receive from channel
- pidをもって、createしたプロセスがatexitでchannelをclose, unlink
- prefixをsuffixに変更
- マシンをまたいだ通信でやり取りするためにバッファの送受信を実装
- 格納するデータを勘案
    - dtype マスト
    - shape マスト
    - buffer マスト
    - 配列長 大きいvolumeに小さいデータを流すには必要
    - pid 解放時に必要だが、マシンをまたぐ場合はこの情報は上書きされる
    - 最後に変更されたunixtime 変更チェックにこれを使うと良い？
        - reciever側が、保持しているデータをupdateするべきか判定できればよい。
- send to channelが持つべき引数
    - if channel is already exist
        - raise error
        - create channel
        - send data if buffer <= volume 
- receive from channel
    - if channel is not exist
        - raise error
        - wait until channel is open
""".strip()


data_format_t = Literal[
    "numpy",
    "pytorch",
    "PIL",
]
data_format_list = data_format_t.__args__


class Transceiver:
    def __init__(self):
        # SharedMemoryオブジェクトを保持する辞書
        # 関数を抜けるなどで SharedMemory オブジェクトが削除される際に、
        # まだそのメモリに対する参照が残っている場合BufferErrorが発生する。
        # クリーンアップはこのクラスで管理するのでshmへの参照は保持する
        self.shm: dict[str, shared_memory.SharedMemory] = {}

    @staticmethod
    def p(name: str) -> str:
        """管理を容易にするために共通するsuffixを付ける"""
        return f"{name}.transceiver"

    def release(self, name: str):
        """
        nameで指定されたshared memoryを解放する
        """
        shm = shared_memory.SharedMemory(name=self.p(name))
        shm.close()
        shm.unlink()

    def read_numpy(self, name: str) -> np.ndarray:
        """
        shared memoryからnumpy arrayを読み込む
        メモリ上で共有されたnumpy arrayを作成して返す
        """
        pname = self.p(name)
        try:
            self.shm[pname] = shared_memory.SharedMemory(name=self.p(name))
        except FileNotFoundError as err:
            raise RuntimeError(f"{name}が存在していません") from err

        serialized_data_field_nbytes = self.shm[pname].buf[-utils.offset_nbytes :]
        data_field_nbytes = utils.length_from_bytes(serialized_data_field_nbytes)
        data_field = utils.data_field_from_buffer(
            self.shm[pname].buf[
                -(data_field_nbytes + utils.offset_nbytes) : -utils.offset_nbytes
            ]
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
            buffer=self.shm[pname].buf[: -(data_field_nbytes + utils.offset_nbytes)],
        )
        return shared_array

    def write_numpy(self, name: str, array: np.ndarray):
        """
        shared memoryにnumpy arrayを書き込む
        メモリ上で共有されたnumpy arrayを作成して返す
        共有されたarrayのshapeやdtypeの変更などは即時には反映されない
        """
        pname = self.p(name)
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
        self.shm[pname] = shared_memory.SharedMemory(
            create=True,
            size=array.nbytes + data_field_nbytes + utils.offset_nbytes,
            name=self.p(name),
        )

        # write numpy buffer
        shared_array = np.ndarray(
            array.shape,
            dtype=array.dtype,
            buffer=self.shm[pname].buf[: -(data_field_nbytes + utils.offset_nbytes)],
        )
        np.copyto(shared_array, array)

        # write data field
        self.shm[pname].buf[
            -(data_field_nbytes + utils.offset_nbytes) : -utils.offset_nbytes
        ] = serialized_data_field

        # write offset
        self.shm[pname].buf[-utils.offset_nbytes :] = serialized_data_field_nbytes


transceiver = Transceiver()
