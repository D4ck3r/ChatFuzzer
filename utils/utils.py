import logging
import hashlib
import asyncio
import configparser
from utils.linked_node import AsyncCircularLinkedList
from utils.priority_queue import AsyncPriorityQueue
import uuid

raw_http_queue = None
seed_template_queue = None
seed_send_queue = None
seed_template_link = None
gpt_chat_queue = None
global_config = None
session = None
global_dict = {}

async def init_raw_http_queue():
    global raw_http_queue
    raw_http_queue = asyncio.Queue()

async def init_gpt_chat_queue():
    global gpt_chat_queue
    gpt_chat_queue = asyncio.Queue()

async def init_seed_template_queue():
    global seed_template_queue
    seed_template_queue = AsyncPriorityQueue()

async def init_seed_send_queue():
    global seed_send_queue
    seed_send_queue = AsyncPriorityQueue()

async def init_seed_template_link():
    global seed_template_link
    seed_template_link = AsyncCircularLinkedList()

def calculate_md5(text):
    md5_obj = hashlib.md5()
    md5_obj.update(text.encode('utf-8'))
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
                        filename='../project.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)