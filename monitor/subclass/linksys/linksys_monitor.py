from monitor.interface.monitor_interface import MonitorInterface
import logging
import re

class LinksysMonitor(MonitorInterface):
    def __init__(self) -> None:
        pass

    def check_login(self, response):
        is_redirect  = False
        if response == "":
            logging.info("check login 302 ")
            is_redirect = True
        else:
            is_redirect = "401 Unauthorized" in response
        return is_redirect

    def restruct_session(self, session, package):
        return re.sub(r"Authorization: Basic .*", b"Authorization: Basic " + session, package)

    def extract_session(self, response):
        session = "OmFkbWlu"
        return session.encode("utf-8")
