from monitor.interface.monitor_interface import MonitorInterface
import logging
import re

class TendaMonitor(MonitorInterface):
    def __init__(self) -> None:
        pass
    
    def check_login(self, response):
        is_redirect = "302 Redirect" in response.splitlines()[0]
        logging.info("check login 302 ")
        return is_redirect
    
    def restruct_session(self, session, package):
        return re.sub(rb"Cookie: .*", b"Cookie: " + session, package)


    def extract_session(self, response):
        session_regex = re.search(r"Set-Cookie: (.*)", response)
        session = session_regex.group(1) if session_regex else None
        return session.encode("utf-8")