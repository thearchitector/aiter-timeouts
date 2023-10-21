import asyncio
from contextlib import nullcontext

import pytest

from aiter_timeouts import IterationTimeoutError, IteratorTimeoutError, with_timeout


async def async_iter(count):
    for i in range(count):
        await asyncio.sleep(1)
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
            async for v in with_timeout(
                async_iter(count), timeout=total, timeout_per_step=step
            )
        ]
        assert res == list(range(count))
