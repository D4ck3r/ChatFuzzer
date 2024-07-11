import asyncio
from utils import utils
from sender.sender import Sender
import logging
import aiofiles
import os 
import pickle 

class Fuzzer:
    def __init__(self) -> None:
        self.config = utils.global_config
        host = self.config[self.config["Fuzzer"]["name"]]["host"]
        port = int(self.config[self.config["Fuzzer"]["name"]]["port"])
        self.timeout = int(self.config["Fuzzer"]["timeout"])
        self.sender = Sender(host,port)
        self.header_send_queue = None
        self.content_send_queue = None
        self.send_seed_lock = asyncio.Lock()
    
    def content_fuzzer(self, data):
        self.sender.send_http_request()

    async def header_fuzzer(self, data):
        response = None
        is_redirect = None
        try:
            response = await self.sender.send_http_request(data, utils.session, timeout = self.timeout, fssl = utils.fssl)
            async with self.send_seed_lock:
                utils.display.send_seed_num += 1
        except ConnectionResetError as e:
            logging.info(f"Connection was reset by peer - {e}")
            utils.vul_package.append(data)
            await utils.vul_package_queue.put(data)
        
        if response and utils.monitor_instance.check_login(response):
            await self.header_send_queue.put(data)
        # print(response)

    async def process_item(self, item):
        if utils.global_config["Fuzzer"]["model"] == "DEBUG":
            filename = utils.calculate_md5(item)
            async with aiofiles.open(os.path.join(utils.global_config["Fuzzer"]["debug_dir_seed"], filename), 'wb') as file:
                await file.write(pickle.dumps(item))
        # logging.info(item)
        await self.header_fuzzer(item)
        logging.info("fuzzer process_item")

    async def consume(self, queue, index, fuzz_type):
        while True:
            logging.info(fuzz_type + "fuzzer begain")
            item = await queue.get()
            # logging.info("Priority: %s"%(item.priority))
            await self.process_item(item)
            # await asyncio.sleep(3)
            logging.info(f"{fuzz_type} Consumer {index} processed an item")

    async def task(self, header_send_queue, content_send_queue):
        self.header_send_queue = header_send_queue
        self.content_send_queue = content_send_queue
        header_consumers = [asyncio.create_task(self.consume(header_send_queue, index, "header")) for index in range(100)]
        content_consumers = [asyncio.create_task(self.consume(content_send_queue, index, "content")) for index in range(100)]
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(*header_consumers, *content_consumers) 