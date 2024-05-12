import asyncio
import logging 
from utils import utils
class Mutator:
    def __int__(self):
        pass

    def num_mutator(self):
        pass

    def str_mutator(self):
        pass
    def process_item(self, item):
        logging.info("mutator process_item")

    async def consume(self, queue, index):
        while True:
            # 从队列中获取项目
            logging.info("mutator begain")
            item = await queue.get_item()
            # item = 1 
            # item = utils.seed_temple_queue.get_item()
            logging.info("123123123123123123")

            # 在线程池中处理项目
       # 直接在协程中处理项目
            self.process_item(item)
            logging.info(f"Consumer {index} processed an item")
    async def test(self):
        while True:
            await asyncio.sleep(3)
            logging.error("Mutator testing")

    async def task(self, queue):
        consumers = [asyncio.create_task(self.consume(queue, index)) for index in range(3)]
        test = [asyncio.create_task(self.test()) for _ in range(5)]

        await asyncio.gather(*consumers, *test)