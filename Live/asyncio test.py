import asyncio
import time


async def main():
    print("a")
    asyncio.sleep(1)
    await func2()

async def func2():
    print("b")

def func3():
    print("c")
    asyncio.sleep(3)

asyncio.run(main())