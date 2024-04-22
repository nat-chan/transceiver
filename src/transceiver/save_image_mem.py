#!/usr/bin/env python3
import atexit
import uuid
from multiprocessing import shared_memory

import comfy_annotations
import numpy as np
import torch
from comfy_annotations import ComfyFunc, ImageTensor, StringInput

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

MANAGED_NAME = set()


@ComfyFunc(
    category="Image",
    display_name="SaveImageMem",
    is_output_node=True,
    debug=True,
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
        try:
            shm = shared_memory.SharedMemory(name=name)
            shm.close()
            shm.unlink()
        except FileNotFoundError:
            pass
        shm = shared_memory.SharedMemory(create=True, size=array.nbytes, name=name)
        shared_array = np.ndarray(array.shape, dtype=array.dtype, buffer=shm.buf)
        np.copyto(shared_array, array)

    original_array = image.detach().cpu().numpy()
    shape_array = np.asarray(original_array.shape, dtype=np.uint8)
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


@ComfyFunc(
    category="Image", display_name="LoadImageMem", is_output_node=False, debug=True
)
def load_image_mem(
    name: str = StringInput("ComfyUI", multiline=False),
) -> ImageTensor:
    """
    nameで指定された画像をshared memoryから読み込む
    """.strip()
    global MANAGED_NAME
    data_shm = shared_memory.SharedMemory(name=f"{name}.data")
    shape_shm = shared_memory.SharedMemory(name=f"{name}.shape")
    shape_array = np.ndarray(shape=[-1], dtype=np.uint8, buffer=shape_shm.buf)
    #    print("="*10)
    #    print(shape_array)
    shared_array = np.ndarray(shape=shape_array, dtype=np.uint8, buffer=data_shm.buf)
    tensor_image = torch.tensor(shared_array)
    return tensor_image


@ComfyFunc(
    category="Image",
    display_name="TestImageMem",
    is_output_node=True,
    debug=True,
)
def test_image_mem(
    image: ImageTensor,
) -> ImageTensor:
    name = str(uuid.uuid4())
    array = image.detach().cpu().numpy()

    shm = shared_memory.SharedMemory(
        create=True, size=array.nbytes, name=f"{name}.data"
    )

    print(array.nbytes)

    shared_array = np.ndarray(array.shape, dtype=array.dtype, buffer=shm.buf)
    np.copyto(shared_array, array)

    shm2 = shared_memory.SharedMemory(name=f"{name}.data")
    shared_array2 = np.ndarray(shape=array.shape, dtype=array.dtype, buffer=shm2.buf)

    tensor_image = torch.tensor(shared_array2)
    return tensor_image


NODE_CLASS_MAPPINGS.update(comfy_annotations.NODE_CLASS_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(comfy_annotations.NODE_DISPLAY_NAME_MAPPINGS)
