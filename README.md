# aiter-timeouts

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/thearchitector/aiter-timeouts/ci.yaml?label=tests&style=flat-square)
![PyPI - Downloads](https://img.shields.io/pypi/dw/aiter-timeouts?style=flat-square)

Timeout functionality for asynchronous iterators. Supports timeouts on the total time to exhaust an asynchronous iterator, or the time it takes for any given step.

Supports Python 3.7+.

## Example

Just wrap your async iterator in a call to `with_timeout`, like so:

```python
from aiter_timeouts import with_timeout

async def async_iter():
    for i in range(10):
        await asyncio.sleep(0.5)
        yield i

try:
    async for val in with_timeout(async_iter(), timeout=6, timeout_per_step=1):
        ...
except IterationTimeoutError as e:
    print(f"step {e.step} took too long")
except IteratorTimeoutError as e:
    print(f"only reached step {e.step} before timing out")
```

## License

MIT License
Copyright (c) 2023 Elias Gabriel
