#!/usr/bin/env python3
import comfy_annotations
from comfy_annotations import ComfyFunc, ImageTensor, MaskTensor, NumberInput, Choice, StringInput
import numpy as np
from multiprocessing import shared_memory
import atexit

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

MANAGED_NAME = set()

@ComfyFunc(
    category="Image",
    display_name="SaveImageMem",
    is_output_node=False,
    debug=True
)
def save_image_mem(
        image: ImageTensor, 
        name: str = StringInput("ComfyUI", multiline=False),
    ):
    """
    画像を入力としてうけつけ、shared memoryを作成する
    """.strip()
    global MANAGED_NAME
    def _save(array: np.ndarray, name: str) -> None:
        # TODO nameが既に存在する場合を考慮していない
#        try:
#            shm = shared_memory.SharedMemory(name=name)
#        except FileNotFoundError:
#            pass
        shm = shared_memory.SharedMemory(create=True, size=array.nbytes, name=name)
        shared_array = np.ndarray(array.shape, dtype=array.dtype, buffer=shm.buf)
        np.copyto(shared_array, array)
    original_array = image.detach().cpu().numpy()
    shape_array = np.ndarray(original_array.shape, dtype=np.uint8)
    _save(original_array, f"{name}.data")
    _save(shape_array, f"{name}.shape")
    MANAGED_NAME.add(name)

def release(name: str) -> None:
    """
    nameで指定されたshared memoryをクリーンアップ
    """.strip()
    shm = shared_memory.SharedMemory(name=name)
    shm.close()
    shm.unlink()

@atexit.register
def release_all() -> None:
    """
    プログラム終了時にsave_image_memで作成された全てのshared memoryを解放
    """
    global MANAGED_NAME
    for name in MANAGED_NAME:
        release(f"{name}.data")
        release(f"{name}.shape")

NODE_CLASS_MAPPINGS.update(comfy_annotations.NODE_CLASS_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(comfy_annotations.NODE_DISPLAY_NAME_MAPPINGS)