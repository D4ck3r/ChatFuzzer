import asyncio
from mutator.structure.seed_template import SeedTemplate
from utils import utils
from sender.sender import Sender
import logging
import aiofiles
import os 
import pickle 
from generate.rawhttp_feature_extraction import split_http_request
import copy 

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
        package = data["package"]
        response = b''
        is_redirect = None
        try:
            response = await self.sender.send_http_request(package, utils.session, timeout = self.timeout, fssl = utils.fssl)
            async with self.send_seed_lock:
                utils.display.send_seed_num += 1
        except ConnectionResetError as e:
            logging.info(f"Connection was reset by peer - {e}")
            utils.vul_package.append(package)
            await utils.vul_package_queue.put(package)

        # if response and utils.monitor_instance.check_login(response): # check login status
        #     await self.header_send_queue.put(data)
        return response
        # print(response)

    async def header_fuzzer(self, data):
        package = data["package"]
        response = b''
        is_redirect = None
        try:
            response = await self.sender.send_http_request(package, utils.session, timeout = self.timeout, fssl = utils.fssl)
            async with self.send_seed_lock:
                utils.display.send_seed_num += 1
        except ConnectionResetError as e:
            logging.info(f"Connection was reset by peer - {e}")
            utils.vul_package.append(package)
            await utils.vul_package_queue.put(package)
        # if response and utils.monitor_instance.check_login(response): # check login status
        #     await self.header_send_queue.put(data)
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
            response = await self.header_fuzzer(item)
        elif ftype == "content":
            response = await self.content_fuzzer(item)
        # logging.error(item['package'])
        # logging.error(response)
        if response == None:
            response = b''
        header, content = split_http_request(response.decode())
        res_md5 = utils.calculate_md5(content)

        if response != b'' and res_md5 not in utils.all_tp_dict[item["id"]].response and "302 Redirect" not in header and len(item["mutation"]) < 20: # create new seed template
            utils.all_tp_dict[item["id"]].response.append(res_md5)
            temp_sp: SeedTemplate = copy.deepcopy(utils.all_tp_dict[item["id"]])
            temp_sp.renew_object(item["index"], ftype)
            new_id = utils.generate_uuid4()
            temp_sp.set_id(new_id)
            temp_sp.times = 0
            await temp_sp.save_to_file(os.path.join(utils.global_config["Fuzzer"]["debug_dir_template"], new_id), response=response,mutation=item)
            utils.all_tp_dict[item["id"]].child_dict[new_id] = temp_sp
            utils.all_tp_dict[new_id] = temp_sp
            utils.display.template_num += 1
            utils.display.temlates_vars["Leaf ST"] += 1
        # logging.info("fuzzer process_item")

    async def consume(self, queue, index, fuzz_type, session_event):
        await asyncio.sleep(3)
        while True:
            await session_event.wait()
            await utils.connect_count.increment()
            item = await queue.get()
            # logging.info("Priority: %s"%(item.priority))
            await self.process_item(item, ftype=fuzz_type) # item <- {"id": fields_array.map_id, "package": package, "index": index, "mutation": item}
            # await asyncio.sleep(3)
            # logging.info(f"{fuzz_type} Consumer {index} processed an item")
            await utils.connect_count.decrement()

    async def task(self, header_send_queue, content_send_queue, session_event):
        self.header_send_queue = header_send_queue
        self.content_send_queue = content_send_queue
        header_consumers = [asyncio.create_task(self.consume(header_send_queue, index, "header", session_event)) for index in range(0)]
        content_consumers = [asyncio.create_task(self.consume(content_send_queue, index, "content", session_event)) for index in range(3)]
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(*header_consumers, *content_consumers)