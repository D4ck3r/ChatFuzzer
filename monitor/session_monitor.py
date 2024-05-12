from utils import utils
import time
from sender.sender import Sender
import asyncio
import re
import logging
class SessionMonitor:
    def __init__(self) -> None:
        self.config = utils.global_config
        self.login_package = self.config["Login-Information"]["loginfile"]
        self.check_package = self.config["Login-Information"]["checkfile"]
        host = self.config["Login-Information"]["host"]
        port = int(self.config["Login-Information"]["port"])
        self.sender = Sender(host,port)

    def get_package(self, filename):
        try:
            with open(filename, 'rb') as file:
                content = file.read()
            return content.decode()
        except FileNotFoundError:
            return "File not found"
        except Exception as e:
            return f"An error occurred: {str(e)}"
        

    async def session_check(self):
        logging.info("send login_check package")
        data = self.get_package(self.check_package)
        while True:
            await asyncio.sleep(3)  # Non-blocking sleep
            response = await self.sender.send_http_request(data, utils.session)
            if response:
                is_redirect = "302 Redirect" in response.splitlines()[0]
            else:
                continue
            if is_redirect:
                await self.session_login()
            else:
                logging.info("login holding")

    async def session_login(self):
        logging.info("send login package")
        data = self.get_package(self.login_package)
        response = await self.sender.send_http_request(data)
        session_regex = re.search(r"Set-Cookie: (.*)", response)
        session = session_regex.group(1) if session_regex else None
        if session:
            utils.session = session
        print(session)

    async def manage_sessions(self):
        # Assume you want to run these concurrently
        # await asyncio.gather(
        #     self.session_check(),
        #     self.session_login()
        # )
        await self.session_check()
