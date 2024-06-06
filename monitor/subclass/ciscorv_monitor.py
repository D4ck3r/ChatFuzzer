from monitor.interface.monitor_interface import MonitorInterface
import logging
import re

class CiscoRVMonitor(MonitorInterface):
    def __init__(self) -> None:
        pass
    
    def check_login(self, response):
        is_redirect = "Login Page" in response
        logging.info("check login 302 ")
        return is_redirect
    
    def restruct_session(self, session, package):
        pattern = r"(\b[A-Z]+\b)\s+([^\s]+)(\s+HTTP\/\d\.\d)"
        replacement = lambda match: f"{match.group(1)} {match.group(2)};session_id={session}{match.group(3)}" \
        if '?' in match.group(2) else \
        f"{match.group(1)} {match.group(2)}?session_id={session_id}{match.group(3)}"
        modified_data, count = re.subn(pattern, replacement, package, 1)
        print(modified_data)
        return modified_data

    def extract_session(self, response):
        url = None
        pattern = rb'document\.location\.href = "([^"]+;session_id=[a-f0-9]+)"'
        match = re.search(pattern, response)
        if match:
            url = match.group(1)
            return url
        else:
            return b''