# test.py
import asyncio
from utils import utils
from generate.rawhttp_feature_extraction import feature_extraction


async def consumers():
    while True:
        item = await utils.raw_http_queue.get()
        if item is None:
            break
        # print(f'Consumed {item}')
        hash_key,res,flag,raw_split = feature_extraction(item)
        if hash_key in utils.global_dict:
            print("exist")
        elif flag:
            pass
        else:
            print("add")
            utils.global_dict[hash_key] = {"rawhttp":item,"feature_content":res,"head_content":raw_split,"hash":hash_key}
            await utils.gpt_chat_queue.put(utils.global_dict[hash_key])
        utils.raw_http_queue.task_done()

async def main():

    await utils.raw_http_queue.put("test")
    await utils.raw_http_queue.put(None)
    await consumers()

if __name__ == "__main__":
    asyncio.run(main())



