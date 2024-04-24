# Transceiver📡

Please see [**comfyui-transceiver**](https://github.com/nat-chan/comfyui-transceiver),  the ComfyUI custom nodes binding of the "transceiver" library.


"transceiver" is a python library that swiftly exchanges fundamental data structures, specifically numpy arrays, between processes, optimizing AI inference tasks that utilize ComfyUI.

## Why?

When processing a large number of requests, the SaveImage and LoadImage nodes may be IO-limited, and using shared memory improves performance by passing images only through memory access, not through IO.

## Installation

The "transceiver" is indexed by PyPI. You can easily integrate it into any project.

```bash
pip install transceiver
```

## Features


UNDER CONSTRUCTION

See [core.py](/src/transceiver/core.py) doc