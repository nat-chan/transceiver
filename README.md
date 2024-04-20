# comfyui-in-memory-transceiver
When processing a large number of requests, the SaveImage and LoadImage nodes may be IO-limited, and using shared memory improves performance by passing images only through memory access, not through IO.
