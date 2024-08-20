import asyncio
import logging 
from mutator.structure.seed_template import SeedTemplate
from utils import utils
from pyradamsa import Radamsa
from mutator.basic import mutation_strategy

class Mutator:
    def __init__(self):
        self.rad = Radamsa()
        self.ms = mutation_strategy.MutationStrategy()
        self.templated_lock = asyncio.Lock()
        self.seed_lock = asyncio.Lock()

    async def header_mutator(self, data: SeedTemplate): # data <- seed template
        # logging.info("mutator header: ")
        for index in data.header_mutate_array:
            res = self.ms.mutator(data.header_marked_fields[index][0], data.header_marked_fields[index][1])
            # res.extend(self.ms.radamsa_mutator(value, 100))
            res.extend(self.ms.inject_mutator(data.map_id))
            await self.header_reconstruct(data, index, res)

    async def content_mutator(self, data: SeedTemplate): # data <- seed template
        # rad = Radamsa()
        # muta_data = self.rad.fuzz(data.encode("utf-8"))
        # logging.info("mutator content: ")
        # print(data.content_marked_fields)
        # for index, (value, type_, count) in enumerate(data.content_marked_fields):
        for index in data.content_mutate_array:
            res = self.ms.mutator(data.content_marked_fields[index][0], data.content_marked_fields[index][1])
            # res.extend(self.ms.radamsa_mutator(value, 100))
            res.extend(self.ms.inject_mutator(data.map_id))
            await self.content_reconstruct(data, index, res)

    async def content_reconstruct(self, fields_array: SeedTemplate, index, res):  # fields_array <- seed template
        for item in res:
            recover = fields_array.content_marked_fields[index][0]
            fields_array.content_marked_fields[index][0] = item
            package = fields_array.reconstruct_packet()
            temp_data = {"id": fields_array.id, "package": package, "index": index, "mutation": item}
            await utils.content_send_queue.put(temp_data)
            async with self.seed_lock:
                utils.display.seed_num += 1
            fields_array.content_marked_fields[index][0] = recover
        
    async def header_reconstruct(self, fields_array: SeedTemplate, index, res): # fields_array <- seed template
        for item in res:
            recover = fields_array.header_marked_fields[index][0]
            fields_array.header_marked_fields[index][0] = item
            package = fields_array.reconstruct_packet()
            temp_data = {"id": fields_array.id, "package": package, "index": index, "mutation": item}
            await utils.header_send_queue.put(temp_data)
            async with self.seed_lock:
                utils.display.seed_num += 1
            fields_array.header_marked_fields[index][0] = recover

    async def process_item(self, item):
        # logging.info(item)
        async with self.templated_lock:
            utils.display.temlates_vars["Templates Processed"] += 1
        await self.content_mutator(item)
        await self.header_mutator(item)
        # print(item)
        # logging.info("mutator process_item")

      

    async def consume(self, queue, index):
        while True:
            # logging.info("mutator begain")
            item = await queue.get_item()
            # logging.info("Priority: %s"%(item.priority))
            await self.process_item(item)
            # await asyncio.sleep(3)
            # logging.info(f"Consumer {index} processed an item")
            # await queue.put_item(item, 2)

    async def test(self):
        while True:
            await asyncio.sleep(3)
            logging.error("Mutator testing")

# queue <- seed_template_queue
    async def task(self, queue):
        consumers = [asyncio.create_task(self.consume(queue, index)) for index in range(3)]
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(*consumers)
