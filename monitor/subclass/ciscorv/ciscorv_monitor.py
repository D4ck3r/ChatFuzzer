from monitor.interface.monitor_interface import MonitorInterface
import logging
import re

class CiscoRVMonitor(MonitorInterface):
    def __init__(self) -> None:
        pass
    
    def check_login(self, response):
        is_redirect = b"Login Page" in response
        if is_redirect:
            logging.info("check login 302 ")
        return is_redirect
    
    def restruct_session(self, session, package):
        # 使用正则表达式匹配并替换 session_id
        pattern = rb"(session_id=)[a-f0-9]{32}"
        replacement = session
        modified_data, count = re.subn(pattern, replacement, package, 1)
        return modified_data

    def extract_session(self, response):
        url = None
        pattern = rb'document\.location\.href = "[^"]+;(session_id=[a-f0-9]+)"'
        match = re.search(pattern, response)
        if match:
            url = match.group(1)
            return url
        else:
            return b''