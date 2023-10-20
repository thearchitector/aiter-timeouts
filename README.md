# aiter-timeouts

Timeout functionality for asynchronous iterators. Supports timeouts on the total time to exhaust an asynchronous iterator, or the time it takes for any given step.

## Example

Just wrap your async iterator in a call to `timeout`, like so:

```python
from aiter_timeouts import timeout

async def async_gen():
    for i in range(10):
        await asyncio.sleep(0.5)
        yield i

try:
    async for val in timeout(async_gen(), timeout=6, timeout_per_step=1):
        ...
except IterationTimeoutError as e:
    print(f"step {e.step} took too long")
except IteratorTimeoutError as e:
    print(f"only reached step {e.step} before timing out")
```

## License

MIT License
Copyright (c) 2023 Elias Gabriel
