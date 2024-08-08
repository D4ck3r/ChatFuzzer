import asyncio

async def task(id, start_event):
    print(f'任务 {id} 正在等待启动信号...')
    await start_event.wait()  # 等待事件被设置
    print(f'任务 {id} 开始执行!')
    # 执行某些工作
    await asyncio.sleep(1)  # 模拟工作耗时
    print(f'任务 {id} 完成!')

async def main():
    start_event = asyncio.Event()  # 创建一个事件

    # 创建并启动多个任务
    tasks = [asyncio.create_task(task(i, start_event)) for i in range(5)]

    await asyncio.sleep(2)  # 延迟一段时间后发出启动信号
    print('发出启动信号!')
    start_event.set()  # 设置事件，所有等待该事件的协程将被唤醒

    # 等待所有任务完成
    await asyncio.gather(*tasks)

asyncio.run(main())
