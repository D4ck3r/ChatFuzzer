import asyncio
from concurrent.futures import ThreadPoolExecutor
from utils import utils
import random
import time
from mutator.seed_template import SeedTemplate
from gpt.gpt_request import OpenAIChatbot

chatbot_header = OpenAIChatbot(config_file="config.ini", chat_type="header")
chatbot_content = OpenAIChatbot(config_file="config.ini", chat_type="content")


async def generate_seed_template(item,label_head,label_content):
    seedtemplate = SeedTemplate(priority = 1)
    seedtemplate.set_id(utils.generate_uuid4())
    seedtemplate.set_label_header(label_head)
    seedtemplate.set_label_content(label_content)
    # print(label_head)
    # print(label_content)
    await utils.seed_template_queue.put_item(seedtemplate, priority=1)

async def process_item(item, queue):
    '''
    {"rawhttp":item,
    "feature_content":res,
    "head_content":raw_split,
    "hash":hash_key}

    :param item:
    :return:
    '''
    head = item["head_content"]["header"]
    content = item["head_content"]["content"]
    label_head = ''
    label_content = ''
    if head:
        label_head = await chatbot_header.chat(head)
    if content:
        label_content = await chatbot_content.chat(content)

    if label_head == "error" or label_content == "error":
        await queue.put(item)
        if item['hash'] in utils.global_dict:
            utils.global_dict.pop(item['hash'])
    await generate_seed_template(item, label_head, label_content)
    print(item["hash"])


async def consume(queue, index):
    while True:
        # 从队列中获取项目
        item = await queue.get()
        if item is None:
            # None 是停止信号
            queue.task_done()
            break
        # 在线程池中处理项目
        await process_item(item, queue)
        queue.task_done()

# async def adds(queue):
#     for item in range(10):
#         await asyncio.sleep(5)  # 使用 asyncio.sleep 而不是 time.sleep
#         await queue.put(item)
#     # 添加停止信号
#     for _ in range(3):
#         await queue.put(None)

async def task(queue):
    consumers = [asyncio.create_task(consume(queue, index)) for index in range(1)]
    await asyncio.gather(*consumers)



# asyncio.run(main())
