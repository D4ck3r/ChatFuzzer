import logging
import hashlib
import asyncio
import configparser
from utils.linked_node import AsyncCircularLinkedList
from utils.priority_queue import AsyncPriorityQueue
import uuid
import aiofiles
import importlib
import os 

raw_http_queue = None
seed_template_queue = None

content_send_queue = None
header_send_queue = None

vul_package_queue = None

monitor_instance = None 

seed_template_link = None
gpt_chat_queue = None
global_config = None
session = None
global_dict = {}
vul_package = []
fssl = None


def init_ssl():
    global fssl, ftype
    ftype = global_config[global_config["Fuzzer"]["name"]]["type"]
    if ftype == "http":
        fssl = None
    elif ftype == "https":
        fssl = True

def init_monitor():
    global monitor_instance
    module = importlib.import_module(global_config[global_config["Fuzzer"]["name"]]["module"])
    class_ = getattr(module, global_config[global_config["Fuzzer"]["name"]]["class_name"])
    monitor_instance = class_()

async def init_raw_http_queue():
    global raw_http_queue
    raw_http_queue = asyncio.Queue()

async def init_gpt_chat_queue():
    global gpt_chat_queue
    gpt_chat_queue = asyncio.Queue()

async def init_seed_template_queue():
    global seed_template_queue
    seed_template_queue = AsyncPriorityQueue()

async def init_content_send_queue():
    global content_send_queue
    content_send_queue = asyncio.Queue()

async def init_header_send_queue():
    global header_send_queue
    header_send_queue = asyncio.Queue()

async def init_vul_package_queue():
    global vul_package_queue
    vul_package_queue = asyncio.Queue()

async def init_seed_template_link():
    global seed_template_link
    seed_template_link = AsyncCircularLinkedList()

async def init_raw_http_queue():
    global raw_http_queue
    raw_http_queue = asyncio.Queue()

def calculate_md5(text):
    md5_obj = hashlib.md5()
    if isinstance(text, str):
        text = text.encode('utf-8')
    md5_obj.update(text)
    return md5_obj.hexdigest()

def generate_uuid4():
    return uuid.uuid4()

def parse_config(filename):
    global global_config 
    global_config = configparser.ConfigParser()
    global_config.read(filename)

def configure_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='project.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


async def write_to_file(filename, content):
    if isinstance(content, str):
        content = content.encode('utf-8')
    try:
        async with aiofiles.open(filename, mode='wb') as file:
            await file.write(content)
        return True  
    except Exception as e:
        logging.error(f"write file  {filename} failed: {e}")
        return False
    


def clear_folder_contents(folder_path):
    # 检查文件夹是否存在
    if os.path.exists(folder_path):
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    os.unlink(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')