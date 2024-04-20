#!/usr/bin/env python3

class SaveImageMem:
    RETURN_TYPES = ("IMAGE", ) # 出力ノードのデータ型
    RETURN_NAMES = ("image", ) # 出力ノード名
    FUNCTION = "run" # ノード実行時に呼ばれる関数名
    OUTPUT_NODE = False # 実行の進んでいく終端ノードとして扱うか
    CATEGORY = "mathbbN" # 左クリックしたときに出てくるカテゴリ
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "shellscript": ("STRING", {"multiline": True}),
                "image": ("IMAGE", {}),
            },
        }

    def run(self, shellscript, image):
        print(shellscript)
        return image

NODE_CLASS_MAPPINGS = { "SaveImageMem": SaveImageMem }
NODE_DISPLAY_NAME_MAPPINGS = { "SaveImageMem": "SaveImageMem" }