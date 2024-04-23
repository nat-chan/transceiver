import ast

import numpy as np

# 2bytesで最大65535-2のフィールドサイズを確保できる。
offset_nbytes = 2
max_length = 2 ** (8 * offset_nbytes) - offset_nbytes

dtypes_list = [
    np.int8,
    np.int16,
    np.int32,
    np.int64,
    np.uint8,
    np.uint16,
    np.uint32,
    np.uint64,
    np.float16,
    np.float32,
    np.float64,
    np.float128,
    np.complex64,
    np.complex128,
    np.complex256,
    np.bool_,
    np.object_,
]

# numpyの利用可能なdtypeは環境依存なのでチェックする
dict_str2dtype = {
    dtype.__name__: dtype for dtype in dtypes_list if hasattr(np, dtype.__name__)
}

dict_dtype2str = {
    dtype: dtype.__name__ for dtype in dtypes_list if hasattr(np, dtype.__name__)
}


def dtype_to_str(array: np.ndarray) -> str:
    """np.ndarrayのdtypeをliteralなstrに変換"""
    return array.dtype.str


def dtype_from_str(dtype: str) -> np.dtype:
    """strからnp.dtypeを復元"""
    return np.dtype(dtype)


def data_field_to_bytes(data_field: dict) -> bytes:
    """
    data_fieldをシリアライズして返す
    dictのkey, valueはliteral_eval()可能なもののみを受け付ける
    """.strip()
    serialized = repr(data_field).encode("utf-8")
    return serialized


def data_field_from_buffer(serialized: memoryview) -> dict:
    """
    シリアライズされたdata_fieldを元に戻す
    """.strip()
    return ast.literal_eval(serialized.tobytes().decode("utf-8"))


def length_to_bytes(length: int) -> bytes:
    """
    literal data fieldの長さを offset_nbytes bytesで表現
    """
    return length.to_bytes(length=offset_nbytes, byteorder="big")


def length_from_bytes(length_bytes: bytes) -> int:
    """
    バッファ末尾からoffset_nbytes取り出したbytesを
    literal data fieldの長さとして解釈して返す
    """
    return int.from_bytes(length_bytes, byteorder="big")
