import asyncio

class AsyncCounter:
    def __init__(self, initial_value=0):
        self.value = initial_value
        self.lock = asyncio.Lock()  # 创建一个锁用于保护对value的操作

    async def increment(self):
        async with self.lock:  # 使用锁来保护增加操作
            self.value += 1

    async def decrement(self):
        async with self.lock:  # 使用锁来保护减少操作
            self.value -= 1
            if self.value < 0:
                self.value = 0  # 确保计数器不会减到负数

    async def is_zero(self):
        async with self.lock:  # 使用锁来保护读取操作
            return self.value == 0

    async def get_value(self):
        async with self.lock:  # 可以添加一个方法来获取当前值
            return self.value