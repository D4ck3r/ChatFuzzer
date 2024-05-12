import asyncio
from concurrent.futures import ThreadPoolExecutor
import random
import time

from gpt.gpt_request import OpenAIChatbot

chatbot = OpenAIChatbot(config_file="config.ini", chat_type="header")
# 定义一个阻塞的任务函数，模拟耗时操作
def process_item(item):
    # time.sleep(random.uniform(0.5, 1.5))  # 模拟耗时操作
    print(chatbot.chat(str(item)))
    print(f"项目 {item} 处理完毕")


# 异步函数，从队列中获取项目并在线程池中处理
async def consume(queue, executor):
    while True:
        # 从队列中获取项目
        item = await queue.get()
        if item is None:
            # None 是停止信号
            queue.task_done()
            break
        # 在线程池中处理项目
        await asyncio.get_running_loop().run_in_executor(executor, process_item, item)
        queue.task_done()
        print(f"项目 {item} 已从队列中移除")


async def adds(queue):
    for item in range(10):
        await asyncio.sleep(5)  # 使用 asyncio.sleep 而不是 time.sleep
        await queue.put(item)

    # 添加停止信号
    for _ in range(3):
        await queue.put(None)


async def main():
    queue = asyncio.Queue()

    # 使用 ThreadPoolExecutor 创建一个线程池
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 创建三个消费者任务
        consumers = [asyncio.create_task(consume(queue, executor)) for _ in range(3)]

        # 运行生产者和消费者任务
        await asyncio.gather(*consumers, adds(queue))


asyncio.run(main())
