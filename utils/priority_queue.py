import queue
import asyncio

class AsyncPriorityQueue:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
        
    async def put_item(self, item, priority):
        await self.queue.put((priority, item))
        # rounded_time = int(time.time() // 5) * 5
        # await self.queue.put((rounded_time, priority, item))        
        # print(f'add：{item}，priority：{priority}')

    async def get_item(self):
        priority, item = await self.queue.get()
        # print(f'deal：{item}，priority：{priority}')
        self.queue.task_done()
        return item
    
    def size(self):
        return self.queue.qsize()

# 使用示例
def main():
    pq = PriorityQueue()

    # 向队列中添加元素
    pq.put_item('低优先级任务', priority=10)
    pq.put_item('高优先级任务1', priority=1)
    pq.put_item('高优先级任务2', priority=1)
    pq.put_item('高优先级任务3', priority=1)
    pq.put_item('高优先级任务4', priority=1)
    pq.put_item('中优先级任务', priority=5)
    pq.put_item('高优先级任务5', priority=1)
    # 从队列中取出元素
    pq.get_item()  # 预期输出: 处理项目：高优先级任务，优先级：1
    pq.get_item()  # 预期输出: 处理项目：中优先级任务，优先级：5
    pq.get_item()  # 预期输出: 处理项目：低优先级任务，优先级：10
    pq.get_item()  # 预期输出: 处理项目：低优先级任务，优先级：10
    pq.get_item()  # 预期输出: 处理项目：低优先级任务，优先级：10
    pq.get_item()  # 预期输出: 处理项目：低优先级任务，优先级：10
    pq.get_item()  # 预期输出: 处理项目：低优先级任务，优先级：10

# asyncio.run(main())
# main()