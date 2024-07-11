import socket
import re
import logging
import asyncio
import ssl
from utils import utils

class Sender:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    async def send_http_request(self, package, session=None, timeout=60, fssl=None):
        writer = None
        response = None  # 初始化 response 为 None
        ssl_context = None
        if fssl:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port, ssl=ssl_context), timeout=timeout)

            if session:
                package = utils.monitor_instance.restruct_session(session, package)
            writer.write(package)
            await writer.drain()

            response = await asyncio.wait_for(reader.read(), timeout=timeout)
        except asyncio.TimeoutError:
            logging.info(f"Operation timed out after {timeout} seconds")
        except ssl.SSLError as e:
            if e.reason == 'APPLICATION_DATA_AFTER_CLOSE_NOTIFY':
                logging.info("SSL close notify received, stopping communication.")
            else:
                logging.error(f"SSL error occurred: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            if writer:
                try:
                    writer.close()
                    await writer.wait_closed()
                except ssl.SSLError as e:
                    if e.reason != 'APPLICATION_DATA_AFTER_CLOSE_NOTIFY':
                        logging.error(f"Error during SSL close: {e}")

        return response
