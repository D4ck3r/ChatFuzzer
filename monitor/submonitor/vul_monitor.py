import asyncio
import logging
from utils import utils
import os 

class VulMonitor():
    def __init__(self) -> None:
        self.config = utils.global_config
        self.save_dir = self.config["Fuzzer"]["vuldir"]

    async def process_item(self, item):
        filename = utils.calculate_md5(item)
        file_path = os.path.join(self.save_dir, filename)
        await utils.write_to_file(file_path, item)
        logging.info("save vul package " + filename)

    async def consume(self, queue, index):
        while True:
            logging.info("VulMonitor begain")
            item = await queue.get()
            await self.process_item(item)

    async def manage_package(self, queue):
        consumers = [asyncio.create_task(self.consume(queue, index)) for index in range(3)]
        await asyncio.gather(*consumers)

