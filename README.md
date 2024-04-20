# comfyui-in-memory-transceiver

## why?

When processing a large number of requests, the SaveImage and LoadImage nodes may be IO-limited, and using shared memory improves performance by passing images only through memory access, not through IO.

## install

```
cd /path/to/ComfyUI
source venv/bin/activate
cd custom_nodes
git clone https://github.com/nat-chan/comfyui-in-memory-transceiver
cd comfyui-in-memory-transceiver
pip install -e .
cd ../.. # cd /path/to/ComfyUI
python main.py # launch
```
## features

### SaveImageMem

todo

### LoadImageMem

todo
