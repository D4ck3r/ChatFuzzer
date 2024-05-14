import asyncio
import logging 
from utils import utils
from pyradamsa import Radamsa
from mutator.basic import mutation_strategy

class Mutator:
    def __init__(self):
        self.rad = Radamsa()
        self.ms = mutation_strategy.MutationStrategy()

    def header_mutator(self, data):
        print(data.header_marked_fields)
        return mutated_data

    def content_mutator(self, data):
        # rad = Radamsa()
        # muta_data = self.rad.fuzz(data.encode("utf-8"))
        logging.info("mutator str: ")
     
        print(data.content_marked_fields)
        for index, (value, type_, count) in enumerate(data.content_marked_fields):
            # single 
            res = self.ms.mutator(value, type_)
            res.extend(self.ms.radamsa_mutator(value, 100))
            self.content_reconstruct(data, index, res)
          
    def content_reconstruct(self, fields_array, index, res):
        for item in res:
            recover = fields_array.content_marked_fields[index][0]
            fields_array.content_marked_fields[index][0] = item
            # data.send_content = temp
            # data.send_header = data.header_marked_fields
            print(fields_array.reconstruct_packet())
            fields_array.content_marked_fields[index][0] = recover
        # return mutated_fields

    # def header_reconstruct(self, fields_array, index, res):
    #     for item in res:
    #         recover = fields_array.content_marked_fields[index][0]
    #         fields_array.content_marked_fields[index][0] = item
    #         # data.send_content = temp
    #         # data.send_header = data.header_marked_fields
    #         print(fields_array.reconstruct_packet())
    #         fields_array.content_marked_fields[index][0] = recover

    def process_item(self, item):
        # logging.info(item)
        self.content_mutator(item)
        print(item)
        logging.info("mutator process_item")

    async def consume(self, queue, index):
        while True:
            logging.info("mutator begain")
            item = await queue.get_item()
            logging.info("Priority: %s"%(item.priority))
            self.process_item(item)
            # await asyncio.sleep(3)
            logging.info(f"Consumer {index} processed an item")
            # await queue.put_item(item, 2)

    async def test(self):
        while True:
            await asyncio.sleep(3)
            logging.error("Mutator testing")

    async def task(self, queue):
        consumers = [asyncio.create_task(self.consume(queue, index)) for index in range(3)]
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(*consumers)