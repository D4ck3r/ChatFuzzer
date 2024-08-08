from monitor.interface.monitor_interface import MonitorInterface
import logging
import re

class TendaMonitor(MonitorInterface):
    def __init__(self) -> None:
        pass
    
    def check_login(self, response):
        is_redirect = b"302 Redirect" in response.splitlines()[0]
        if is_redirect:
            logging.info("check login 302 1")
        return is_redirect
    
    def restruct_session(self, session, package):
        return re.sub(rb"Cookie: .*", b"Cookie: " + session, package)

    def extract_session(self, response):
        session_regex = re.search(rb"Set-Cookie: (.*)", response)
        session = session_regex.group(1) if session_regex else None
        return session