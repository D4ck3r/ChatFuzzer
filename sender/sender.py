import socket
import re
import logging
import asyncio

class Sender:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    # async def send_http_request(self, package, session=None):
    #     self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     try:
    #         await self.socket.connect((self.host, self.port))
    #         if session:
    #             package = re.sub(r"Cookie: .*", f"Cookie: {session}", package)
    #         await self.socket.sendall(package.encode("utf-8"))
    #         response = b''
    #         while True:
    #             part = self.socket.recv(1024)
    #             if not part:
    #                 break
    #             response += part
    #     except ConnectionRefusedError as e:
    #         logging.info(f"Error connecting to {self.host}:{self.port} - {e}")
    #         return None
    #     except socket.error as e:
    #         logging.info(f"Socket error - {e}")
    #         return None
    #     except Exception as e:
    #         logging.info(f"An error occurred - {e}")
    #         return None
    #     finally:
    #         if self.socket:
    #             self.socket.close()
    #     return response.decode()

    async def send_http_request(self, package, session=None):
        writer = None  # 初始化writer为None
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            if session:
                package = re.sub(rb"Cookie: .*", b"Cookie: " + session, package)
            writer.write(package)
            await writer.drain()
            response = await reader.read()
        except ConnectionRefusedError as e:
            logging.info(f"Error connecting to {self.host}:{self.port} - {e}")
            return None
        except Exception as e:
            logging.info(f"An error occurred - {e}")
            return None
        finally:
            if writer:  # 在关闭前检查writer是否存在
                writer.close()
                await writer.wait_closed()
        return response.decode()
# 使用例子
if __name__ == "__main__":
    host = '192.168.0.200'
    port = 80
    package = (
        'POST /login/Auth HTTP/1.1\r\n'
        'Host: 192.168.0.200\r\n'
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0\r\n'
        'Accept: */*\r\n'
        'Accept-Language: en-US,en;q=0.5\r\n'
        'Accept-Encoding: gzip, deflate\r\n'
        'Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n'
        'X-Requested-With: XMLHttpRequest\r\n'
        'Content-Length: 56\r\n'
        'Origin: http://192.168.0.200\r\n'
        'Connection: close\r\n'
        'Referer: http://192.168.0.200/login.html\r\n'
        'Cookie: password=7da188c2e2d83e38b7d9e75e500f1af8rnp5gk\r\n'
        '\r\n'
        'username=admin&password=7da188c2e2d83e38b7d9e75e500f1af8'
    )

    sender = Sender(host, port)
    response = sender.send_http_request(package.encode())
    print(response)
    # while True:
    #     response = sender.send_http_request(package.encode())
    #     print(response)
