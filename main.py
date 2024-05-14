import asyncio
from generate.rawhttp_deal import consumers
from generate.rawhttp_receiver import AsyncRabbitMQConsumer
from gpt.gpt_task import task
from utils import utils
from monitor.session_monitor import SessionMonitor
from mutator.mutator import Mutator
async def main():
    utils.configure_logging()
    utils.parse_config("config.ini")
    await utils.init_seed_template_queue()
    await utils.init_raw_http_queue()
    await utils.init_gpt_chat_queue()
    consumer = AsyncRabbitMQConsumer()
    monitor = SessionMonitor()
    mutator = Mutator()
    await consumer.connect()
   
    rabbit_consumer = asyncio.create_task(consumer.start_consuming())  #receive message from rabbit mq
    producer_task = asyncio.create_task(consumers()) # preduce message and  send to gpt task
    gpt_task = asyncio.create_task(task(utils.gpt_chat_queue)) #gpt task generate seed template
    manage_sessions = asyncio.create_task(monitor.manage_sessions())# check session is alive
    mutator_task = asyncio.create_task(mutator.task(utils.seed_template_queue)) # mutator 
    # fuzzer_task =  asyncio.create_task(mutator.task(utils.seed_template_queue))
    # template_seed_queue_task = asyncio.create_task(consumers())
    # template_seed_link_task = asyncio.create_task(consumers())
    await asyncio.gather(rabbit_consumer, producer_task, gpt_task, manage_sessions, mutator_task)

if __name__ == '__main__':
    asyncio.run(main(), debug=True)
 