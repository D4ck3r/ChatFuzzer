import asyncio
import logging
import os
import aiofiles
from utils import utils
from gpt.gpt_task import chatbot_routercode, chatbot_packagecode
class LLMCodeAnalyse():
    def __init__(self) -> None:
        self.folder_path = utils.global_config["Fuzzer"]["code_data_dir"]
        self.queue = asyncio.Queue()

    async def gptcode_consume(self):
        logging.info("Seed Scheduling began")

        while True:
            response = b''
            item = await self.queue.get()
            file_path, label, content = item
            logging.info(f"File: {file_path}, Label: {label}, Content: {content}")
            self.queue.task_done()
            if label == "route":
                response = await chatbot_routercode.chat(content)
            elif label == "package":
                response = await chatbot_packagecode.chat(content)

            if response == "error":
                await self.queue.put((file_path, label, content))
                continue

            segments = response.split(b"-+-+-+-+")
            for item in segments:
                temp = item.strip()
                print(temp)
            await asyncio.sleep(3)




    async def readfile_consume(self):
        while True:
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                if os.path.isfile(file_path):
                    async with aiofiles.open(file_path, mode='r') as f:
                        content = await f.read()
                        segments = content.split("-+-+-+-+")
                        if len(segments) > 0:
                            first_segment = segments[0].strip()
                            if first_segment.count('\n') == 0:
                                label = 'route'
                            else:
                                label = 'package'
                            logging.error(label)
                            await self.queue.put((file_path, label, content))
                    os.remove(file_path)
                    logging.info(f"Deleted file: {file_path}")
            await asyncio.sleep(1)

    async def task(self):
        readfile_consumer = asyncio.create_task(self.readfile_consume())
        gptcode_consumers = [asyncio.create_task(self.gptcode_consume()) for _ in range(3)]
        await asyncio.gather(*gptcode_consumers, readfile_consumer)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    folder_path = "./your_folder"  # 替换为你要监控的文件夹路径
    analyser = LLMCodeAnalyse(folder_path)
    asyncio.run(analyser.task())
