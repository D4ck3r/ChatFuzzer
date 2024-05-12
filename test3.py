import asyncio
import random

async def produce(queue, item, priority):
    # 模拟异步的生产过程
    await asyncio.sleep(random.uniform(0.1, 1))  # 随机延迟来模拟生产时间
    await queue.put((priority, item))
    print(f'添加了：{item}，优先级：{priority}')

async def consume(queue):
    while True:
        # 获取项目
        priority, item = await queue.get()
        # 模拟异步的消费过程
        await asyncio.sleep(random.uniform(0.1, 1))  # 随机延迟来模拟处理时间
        print(f'处理了：{item}，优先级：{priority}')
        queue.task_done()

async def main():
    queue = asyncio.PriorityQueue()

    # 创建生产者和消费者协程
    producers = [produce(queue, f'任务{i}', random.randint(1, 10)) for i in range(10)]
    consumer = asyncio.create_task(consume(queue))

    # 等待所有生产者协程完成
    await asyncio.gather(*producers)
    # 等待一段时间，确保所有项目都被消费
    await asyncio.sleep(10)
    # 取消消费者协程
    consumer.cancel()
    # 等待消费者协程取消
    await asyncio.gather(consumer, return_exceptions=True)

asyncio.run(main())
