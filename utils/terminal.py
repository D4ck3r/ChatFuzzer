import asyncio
import logging
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.logging import RichHandler
from rich.layout import Layout

class RichLoggerDisplay:
    def __init__(self):
        self.console = Console()
        self.variables = {
            "Variable1": 0,
            "Variable2": 0,
            "Variable3": 0
        }
        self.configure_logging()

    def configure_logging(self):
        # 使用 RichHandler 实现彩色和高亮的日志输出
        rich_handler = RichHandler(
            console=self.console,
            show_time=True,
            show_path=False,
            show_level=True,
            rich_tracebacks=True,
            markup=True
        )
        rich_handler.setLevel(logging.INFO)
        file_handler = logging.FileHandler('project.log')  # 将日志记录到文件
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(message)s",
            handlers=[rich_handler, file_handler]
        )
        self.logger = logging.getLogger('rich_logger')
        self.logger.info("[bold magenta]Logging initialized[/]")

    async def update_variables(self):
        while True:
            self.variables["Variable1"] += 1
            self.variables["Variable2"] += 2
            self.variables["Variable3"] += 3
            self.logger.info(f"[bold green]Updated variables:[/] {self.variables}")
            await asyncio.sleep(1)  # 每秒更新一次

    def render_table(self):
        table = Table(title="[bold cyan]Real-time Variable Display[/]", expand=True)
        table.add_column("[bold green]Variable[/]", justify="right", style="cyan", no_wrap=True)
        table.add_column("[bold yellow]Value[/]", justify="right", style="magenta")
        for key, value in self.variables.items():
            table.add_row(str(key), str(value))
        return table

    async def display(self):
        layout = self.create_layout()
        with Live(layout, refresh_per_second=1, console=self.console) as live:
            while True:
                # 更新 layout 来防止重叠
                layout = self.create_layout()
                live.update(layout)
                await asyncio.sleep(0.1)

    def create_layout(self):
        layout = Layout()
        layout.split(
            Layout(name="table")  # 一个包含表格的固定底部区域
        )
        table = self.render_table()
        layout["table"].update(table)
        return layout
    
    async def run(self):
        variable_task = self.update_variables()
        display_task = self.display()
        await asyncio.gather(variable_task, display_task)

if __name__ == "__main__":
    display = RichLoggerDisplay()
    asyncio.run(display.run())
