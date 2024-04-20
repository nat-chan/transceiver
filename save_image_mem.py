#!/usr/bin/env python3
import comfy_annotations
from comfy_annotations import ComfyFunc, ImageTensor, MaskTensor, NumberInput, Choice, StringInput
from fs.memoryfs import MemoryFS
mem_fs = MemoryFS()
import numpy as np

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

@ComfyFunc(
    category="Image",
    display_name="SaveImageMem",
    is_output_node=True,  # ComfyUI will always run this node
    debug=True
)
def save_image_mem(
        image: ImageTensor, 
        filename_prefix: str = StringInput("ComfyUI", multiline=False),
    ) -> None:
    """
    画像を入力としてうけつけ、指定されたパスのメモリファイルシステムに書きこむ
    """.strip()
    # torch のimageをcpu detachしてnumpy 
    # 
    np_array = image.detach().cpu().numpy()
    with mem_fs.openbin(f"{filename_prefix}.npy", "w") as f:
        np.save(f, np_array)

NODE_CLASS_MAPPINGS.update(comfy_annotations.NODE_CLASS_MAPPINGS)
NODE_DISPLAY_NAME_MAPPINGS.update(comfy_annotations.NODE_DISPLAY_NAME_MAPPINGS)