from monitor.submonitor.session_monitor import SessionMonitor
from monitor.submonitor.vul_monitor import VulMonitor
import asyncio

class Monitor():
    def __init__(self) -> None:
        self.session_monitor = SessionMonitor()
        self.vul_monitor = VulMonitor()

    async def task(self, queue, session_event):
        session_monitor_task = asyncio.create_task(self.session_monitor.manage_sessions(session_event))
        vul_monitor_task = asyncio.create_task(self.vul_monitor.manage_package(queue))
        # test = [asyncio.create_task(self.test()) for _ in range(5)]
        await asyncio.gather(session_monitor_task, vul_monitor_task)