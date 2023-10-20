import asyncio
from contextlib import nullcontext

import pytest

from aiter_timeouts import IterationTimeoutError, IteratorTimeoutError, timeout


async def async_gen():
    for i in range(10):
        await asyncio.sleep(0.5)
        yield i


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "count,total,step,error",
    [
        (1, None, None, None),
        (2, 1, None, IteratorTimeoutError),
        (2, None, 1, IterationTimeoutError),
    ],
)
async def test_async_iter(count, total, step, error):
    context = pytest.raises(error) if error else nullcontext()
    with context:
        res = [
            v
            async for v in timeout(
                async_gen(count), timeout=total, timeout_per_step=step
            )
        ]
        assert res == list(range(count))


try:
    async for val in timeout(async_gen(), timeout=6, timeout_per_step=1):
        ...
except IterationTimeoutError as e:
    print(f"step {e.step} took too long")
except IteratorTimeoutError as e:
    print(f"only reached step {e.step} before timing out")
