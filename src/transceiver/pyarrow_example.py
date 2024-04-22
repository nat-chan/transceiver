import numpy as np
import pyarrow as pa
import pyarrow.ipc as ipc


def create_shared_array(name: str, array: np.ndarray) -> None:
    """
    numpyの配列を共有メモリに保存し、他のプロセスから参照可能にする
    """
    # numpy配列をArrowテンソルに変換
    arrow_tensor = pa.Tensor.from_numpy(array)
    # Arrowテンソルを共有メモリに書き込む
    sink = pa.BufferOutputStream()
    ipc.write_tensor(arrow_tensor, sink)
    buffer = sink.getvalue()
    # 共有メモリオブジェクトを作成し、データを書き込む
    with pa.OSFile(name, "wb") as file:
        file.write(buffer)


def read_shared_array(name: str) -> np.ndarray:
    """
    共有メモリからnumpy配列を読み込む
    """
    # 共有メモリファイルを開く
    with pa.memory_map(name, "r") as mmap:
        # Arrowテンソルを読み込む
        tensor = ipc.read_tensor(mmap)
    # numpy配列に変換
    array = tensor.to_numpy()
    return array


# 使用例
if __name__ == "__main__":
    # 共有メモリに保存するnumpy配列を作成
    original_array = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int32)
    # 配列を共有メモリに保存
    create_shared_array("shared_array", original_array)
    # 共有メモリから配列を読み込む
    loaded_array = read_shared_array("shared_array")
    print("Loaded array:\n", loaded_array)
