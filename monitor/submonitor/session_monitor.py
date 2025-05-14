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

    async def session_check(self, session_event):
        logging.info("send login_check package")
        data = self.get_package(self.check_package)
        response = None
        while True:
            try:
                response = await self.sender.send_http_request(data, utils.session, fssl= utils.fssl, stype="monitor")
            except ConnectionResetError as e:
                logging.info(f"Connection was reset by peer - {e}")
            logging.debug(response)
            if response and utils.monitor_instance.check_login(response):
                await self.session_login(session_event)
            else:
                logging.info("login holding")
            await asyncio.sleep(1)  # Non-blocking sleep

    async def session_login(self, session_event):
        response = None
        session_event.clear()
        await asyncio.sleep(10)
        logging.info("send login package------")

        # logging.error("session_event clear")

        # while True:
        #     if await utils.connect_count.is_zero():
        #         break
        #     # logging.error("wait connection")

        #     await asyncio.sleep(1)
        for item in self.login_package:
            data = self.get_package(item)
            try:
                response = await self.sender.send_http_request(data, fssl= utils.fssl, stype="monitor")
            except ConnectionResetError as e:
                logging.info(f"Connection was reset by peer - {e}")
            if response:
                utils.session = utils.monitor_instance.extract_session(response)
                # await self.session_check()
                if utils.session != None and utils.session != b'':
                    await utils.write_to_file("monitor/session.data", utils.session)
                    logging.info("session === ")
                    logging.info(utils.session)
        
        await asyncio.sleep(10)

        # logging.error()
        session_event.set()
        logging.error("session_event set++++++")


    async def manage_sessions(self, session_event):
        await self.session_check(session_event)
