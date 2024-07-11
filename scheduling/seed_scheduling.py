import asyncio
import logging
import math
from utils import utils

class SeedScheduling():
    def __init__(self) -> None:
        pass

    def select_top_percent(self, seed_templates_dict, percent=20):
        samples = [(key, template.sample_beta()) for key, template in seed_templates_dict.items()]
        samples_sorted = sorted(samples, key=lambda x: x[1], reverse=True)
        top_count = math.ceil(len(samples) * (percent / 100))  # 使用 math.ceil 进行向上取整
        top_count = min(top_count, len(samples))
        top_templates = {key: seed_templates_dict[key] for key, _ in samples_sorted[:top_count]}
        return top_templates

    async def consume(self, queue, index):
        logging.info("Seed Scheduling begain")
        while True:
            if queue.size() < 1000:
                selected_templates = self.select_top_percent(utils.root_tp_dict, 20)
            for _, template in selected_templates.items():
                await queue.put_item(template, 1)
            # await self.process_item(item)
            logging.info(f"Seed Scheduling {index} processed an template")
            await asyncio.sleep(1)

# queue <- seed_template_queue
    async def task(self, queue):
        consumers = [asyncio.create_task(self.consume(queue, index)) for index in range(3)]
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(*consumers)
