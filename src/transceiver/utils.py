import numpy as np


# 2bytesで最大65535-2のフィールドサイズを確保できる。
offset_nbytes = 2

dtypes_list = [
    np.int8, np.int16, np.int32, np.int64,
    np.uint8, np.uint16, np.uint32, np.uint64,
    np.float16, np.float32, np.float64, np.float128,
    np.complex64, np.complex128, np.complex256,
    np.bool_, np.object_
]

# numpyの利用可能なdtypeは環境依存なのでチェックする
dict_str2dtype = {
    dtype.__name__: dtype
    for dtype in dtypes_list
    if hasattr(np, dtype.__name__)
}

dict_dtype2str = {
    dtype: dtype.__name__
    for dtype in dtypes_list
    if hasattr(np, dtype.__name__)
}


def dtype_to_str(array: np.ndarray) -> str:
    """np.ndarrayのdtypeをliteralなstrに変換"""
    return array.dtype.str

def dtype_from_str(dtype: str) -> np.dtype:
    """strからnp.dtypeを復元"""
    return np.dtype(dtype)
     

def test_field():
    array = np.zeros(shape=[10**7], dtype=np.uint8)
    array.shape


#dict_dtype2num = dict()
#{for d in dtypes_list}
