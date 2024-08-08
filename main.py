import asyncio
from generate.rawhttp_deal import consumers
from generate.rawhttp_receiver import AsyncRabbitMQConsumer
from gpt.gpt_code_analyse import LLMCodeAnalyse
from gpt.gpt_task import task
from utils import utils
from monitor.submonitor.session_monitor import SessionMonitor
from monitor.monitor import Monitor
from mutator.mutator import Mutator
from fuzz.fuzzer import Fuzzer
from scheduling.seed_scheduling import SeedScheduling
from utils.system_check import SystemChecker

async def main():
    # utils.configure_logging()
    utils.parse_config("config.ini")
    utils.init_ssl()
    utils.init_monitor()
    await utils.init_seed_template_queue()
    await utils.init_raw_http_queue()
    await utils.init_gpt_chat_queue()
    await utils.init_content_send_queue()
    await utils.init_header_send_queue()
    await utils.init_vul_package_queue()
    consumer = AsyncRabbitMQConsumer()
    monitor = Monitor()
    scheduling = SeedScheduling()
    mutator = Mutator()
    fuzzer = Fuzzer()
    checker = SystemChecker()
    codegpt =  LLMCodeAnalyse()
    results = checker.run_checks()
    await consumer.connect()
    session_event = asyncio.Event()

    # Algorithm 1
    display_task = asyncio.create_task(utils.display.run())
    # display_task1 = asyncio.create_task(utils.display.update_variables())
    rabbit_consumer = asyncio.create_task(consumer.start_consuming())  #receive message from rabbit mq
    producer_task = asyncio.create_task(consumers()) # preduce message and  send to gpt task
    gpt_task = asyncio.create_task(task(utils.gpt_chat_queue)) #gpt task generate seed template
    
    # Algorithm 2
    monitor_task = asyncio.create_task(monitor.task(utils.vul_package_queue, session_event))
    scheduling_task = asyncio.create_task(scheduling.task(utils.seed_template_queue))
    mutator_task = asyncio.create_task(mutator.task(utils.seed_template_queue)) # mutator  seed_template_queue from seed scheduling
    fuzzer_task = asyncio.create_task(fuzzer.task(utils.header_send_queue, utils.content_send_queue, session_event))

    # Code Analyse
    code_task = asyncio.create_task(codegpt.task())
    
    await asyncio.gather(display_task, rabbit_consumer, producer_task, gpt_task, monitor_task, scheduling_task, mutator_task, fuzzer_task, code_task)
    # await asyncio.gather(rabbit_consumer, producer_task, monitor_task, mutator_task, fuzzer_task)
    # await asyncio.gather(monitor_task)
    
if __name__ == '__main__':
    # utils.clear_folder_contents("debug")
    # utils.clear_folder_contents("fuzz/result")
    asyncio.run(main(), debug=True)

