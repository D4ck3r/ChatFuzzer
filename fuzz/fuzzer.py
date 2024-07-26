import asyncio
from utils import utils
from sender.sender import Sender
import logging
import aiofiles
import os 
import pickle 
from generate.rawhttp_feature_extraction import split_http_request

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
    
    async def content_fuzzer(self, data):
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
        
        if response and utils.monitor_instance.check_login(response): # check login status
            await self.header_send_queue.put(data)

        
        return response
        # print(response)

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
        
        if response and utils.monitor_instance.check_login(response): # check login status
            await self.header_send_queue.put(data)

        
        return response
        # print(response)

    async def process_item(self, item, ftype = "header"):
        response = b''
        if utils.global_config["Fuzzer"]["model"] == "DEBUG":
            filename = utils.calculate_md5(item["package"])
            async with aiofiles.open(os.path.join(utils.global_config["Fuzzer"]["debug_dir_seed"], filename), 'wb') as file:
                await file.write(pickle.dumps(item))
        # logging.info(item)
        if ftype == "header":
            response = await self.header_fuzzer(item["package"])
        elif ftype == "content":
            response = await self.content_fuzzer(item["package"])
        
        header, content = split_http_request(response.decode())
        res_md5 = utils.calculate_md5(content)

        if res_md5 not in utils.root_tp_dict[item["id"]].response:
            utils.root_tp_dict[item["id"]].response.append(res_md5)
        # logging.info("fuzzer process_item")

    async def consume(self, queue, index, fuzz_type):
        while True:
            logging.info(fuzz_type + "fuzzer begain")
            item = await queue.get()
            # logging.info("Priority: %s"%(item.priority))
            await self.process_item(item, ftype=fuzz_type) # item <- {"id":id, "package": package}
            # await asyncio.sleep(3)
            logging.info(f"{fuzz_type} Consumer {index} processed an item")

    async def task(self, header_send_queue, content_send_queue):
        self.header_send_queue = header_send_queue
        self.content_send_queue = content_send_queue
        header_consumers = [asyncio.create_task(self.consume(header_send_queue, index, "header")) for index in range(50)]
        content_consumers = [asyncio.create_task(self.consume(content_send_queue, index, "content")) for index in range(10)]
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(*header_consumers, *content_consumers) 