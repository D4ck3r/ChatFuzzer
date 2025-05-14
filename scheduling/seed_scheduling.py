import asyncio
import logging
import math
from mutator.structure.seed_template import SeedTemplate
from utils import utils
from datetime import datetime

class SeedScheduling():
    def __init__(self) -> None:
        pass

    def select_top_percent(self, seed_templates_dict, percent=20):
        utils.display.temlates_vars["Thompson Sampling Round"] += 1
        samples = [(key, template.sample_beta()) for key, template in seed_templates_dict.items()]
        samples_sorted = sorted(samples, key=lambda x: x[1], reverse=True)
        top_count = math.ceil(len(samples) * (percent / 100))  
        top_count = min(top_count, len(samples))
        top_templates = {key: seed_templates_dict[key] for key, _ in samples_sorted[:top_count]}        
        return top_templates
    
    async def select_all_sp(self, seed_templates_dict, queue):
        # logging.error("######start")
        list_queue = asyncio.Queue()
        selected_templates = self.select_top_percent(seed_templates_dict, 20)
        # await asyncio.sleep(1)
        for _, template in selected_templates.items():
            await list_queue.put(template)
        
        while not list_queue.empty():
            item: SeedTemplate = await list_queue.get()
            if utils.all_tp_dict[item.id].times == 0:
                utils.display.unique_template_num += 1
                # logging.error("got 1 "+item.id)
                # logging.error(item.id+"--"+str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] )+"-------")
            utils.all_tp_dict[item.id].times += 1
            # logging.error(item.id+"--"+str(item.times)+'--'+str(utils.all_tp_dict[item.id].times))
            await queue.put_item(item, 1)
            selected_templates_child = self.select_top_percent(item.child_dict, 20)
             
            for _, item1 in selected_templates_child.items():
                await list_queue.put(item1)
        output = ''
        for _, temp in utils.all_tp_dict.items():
            output += temp.id + '|' + str(temp.times) + '\n'
        # logging.error("\n"+output+"######end")

            # list_queue.task_done()


    async def consume(self, queue, index):
        logging.info("Seed Scheduling begain")
        while True:
            await self.select_all_sp(utils.root_tp_dict, queue)
            # if utils.header_send_queue.qsize() + utils.content_send_queue.qsize() < 200  :
            #     selected_templates = self.select_top_percent(utils.root_tp_dict, 20) # select template from root template dictionary, start
            
            # for _, template in selected_templates.items():
            #     if template.times == 0:
            #         utils.display.unique_template_num += 1
            #     template.times += 1
            #     await queue.put_item(template, 1)

            # logging.info(f"Seed Scheduling {index} processed an template")
            await asyncio.sleep(1)

# queue <- seed_template_queue
    async def task(self, queue):
        consumers = [asyncio.create_task(self.consume(queue, index)) for index in range(1)]
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(*consumers)