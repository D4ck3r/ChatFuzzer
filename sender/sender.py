import socket
import re
import logging
import asyncio
import ssl

class Sender:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    async def send_http_request(self, package, session=None, timeout=60, fssl = None):
        writer = None  # 初始化writer为None
        ssl_context = None
        if fssl:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False  # 禁止检查主机名
            ssl_context.verify_mode = ssl.CERT_NONE  # 禁止验证证书

        try:
            # 使用 asyncio.wait_for 添加超时处理
            reader, writer = await asyncio.wait_for(asyncio.open_connection(self.host, self.port,ssl = ssl_context), timeout=timeout)
            if session:
                package = re.sub(rb"Cookie: .*", b"Cookie: " + session, package)
            writer.write(package)
            await writer.drain()
            # 对读取操作也添加超时处理
            response = await asyncio.wait_for(reader.read(), timeout=timeout)
        except asyncio.TimeoutError:
            logging.info(f"Operation timed out after {timeout} seconds")
            return None
        except ConnectionResetError as e:
            logging.info(f"Connection was reset by peer - {e}")
            return None
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
