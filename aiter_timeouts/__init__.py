from __future__ import annotations

import asyncio
import typing

if typing.TYPE_CHECKING:
    from asyncio import AbstractEventLoop
    from typing import AsyncIterator, Optional, TypeVar

    YT = TypeVar("YT")


class IterationTimeoutError(asyncio.TimeoutError):
    """Raised when an individual iteration of an async iterator takes too long."""

    def __init__(self, step: int):
        self.step = step
        super().__init__()


class IteratorTimeoutError(IterationTimeoutError):
    """Raised when an async iterator takes too long to yield all its values."""


async def timeout(
    asynciter: AsyncIterator[YT],
    timeout: Optional[float] = None,
    timeout_per_step: Optional[float] = None,
) -> AsyncIterator[YT]:
    """
    Wraps the provided asynchronous iterator with a full-length iteration timeout, as
    well as a timeout for each step in that iteration.
    """
    loop: AbstractEventLoop = asyncio.get_running_loop()
    iteration_start: float = loop.time()

    step: int = 0
    while True:
        if timeout is not None and loop.time() - iteration_start >= timeout:
            raise IteratorTimeoutError(step)

        try:
            yield await asyncio.wait_for(asynciter.__anext__(), timeout_per_step)
            step += 1
        except asyncio.TimeoutError as e:
            raise IterationTimeoutError(step) from e
        except StopAsyncIteration:
            break
