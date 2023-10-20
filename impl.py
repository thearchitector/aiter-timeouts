import asyncio


async def async_gen():
    for i in range(5):
        await asyncio.sleep(i)
        yield i


class IterationTimeoutError(asyncio.TimeoutError):
    """Raised when an individual iteration of an async iterator takes too long."""

    def __init__(self, step):
        self.step = step
        super().__init__()


class IteratorTimeoutError(asyncio.TimeoutError):
    """Raised when an async iterator takes too long to yield all its values."""


async def timeout(
    async_gen, timeout: float | None = None, timeout_per_step: float | None = None
):
    loop = asyncio.get_running_loop()
    iteration_start: float = loop.time()

    ageniter = async_gen.__aiter__()
    step: int = 0
    while True:
        if timeout is not None and loop.time() - iteration_start >= timeout:
            raise IteratorTimeoutError()

        try:
            yield await asyncio.wait_for(ageniter.__anext__(), timeout_per_step)
            step += 1
        except asyncio.TimeoutError as e:
            raise IterationTimeoutError(step) from e
        except StopAsyncIteration:
            break


async def task():
    try:
        async for value in timeout(async_gen(), timeout=3, timeout_per_step=4):
            yield value
    except IteratorTimeoutError:
        print("whole op")
    except IterationTimeoutError as e:
        print(f"step {e.step}")


async def main():
    async for v in task():
        print(v)


if __name__ == "__main__":
    asyncio.run(main())
