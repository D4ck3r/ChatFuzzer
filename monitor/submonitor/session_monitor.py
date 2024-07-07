from utils import utils
from sender.sender import Sender
import asyncio
import re
import logging
import os 

class SessionMonitor:
    def __init__(self) -> None:
        self.config = utils.global_config
        # login_package array struct
        self.login_package = [item.strip() for item in self.config[self.config["Fuzzer"]["name"]]["loginfile"].split(',')] 
        self.check_package = self.config[self.config["Fuzzer"]["name"]]["checkfile"]
        host = self.config[self.config["Fuzzer"]["name"]]["host"]
        port = int(self.config[self.config["Fuzzer"]["name"]]["port"])
        self.sender = Sender(host,port)

    def get_package(self, filename):
        try:
            with open(filename, 'rb') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return "File not found"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    async def session_check(self):
        logging.info("send login_check package")
        data = self.get_package(self.check_package)
        response = None
        while True:
            await asyncio.sleep(3)  # Non-blocking sleep
            try:
                response = await self.sender.send_http_request(data, utils.session, fssl= utils.fssl)
            except ConnectionResetError as e:
                logging.info(f"Connection was reset by peer - {e}")

            if response and utils.monitor_instance.check_login(response):
                await self.session_login()
            else:
                logging.info("login holding")

    async def session_login(self):
        response = None
        logging.info("send login package")
        
        for item in self.login_package:
            data = self.get_package(item)
            try:
                response = await self.sender.send_http_request(data, fssl= utils.fssl)
            except ConnectionResetError as e:
                logging.info(f"Connection was reset by peer - {e}")
            if response:
                utils.session = utils.monitor_instance.extract_session(response)
                if utils.session != None and utils.session != b'':
                    await utils.write_to_file("monitor/session.data", utils.session)

    async def manage_sessions(self):
        # Assume you want to run these concurrently
        # await asyncio.gather(
        #     self.session_check(),
        #     self.session_login()
        # )
        await self.session_check()
