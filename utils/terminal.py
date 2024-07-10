import asyncio
import logging
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.logging import RichHandler
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.box import ROUNDED
from datetime import datetime, timedelta

class RichLoggerDisplay:
    def __init__(self, global_config):
        self.global_config = global_config
        self.start_time = datetime.now()
        self.console = Console()
        product = self.global_config[self.global_config["Fuzzer"]["name"]]
        self.temlates_vars = {
            "Seed Templates": 0,
            "Seeds": 0,
            "Root ST": 0,
            "Leaf ST": 0,
            "Thompson Sampling Round": 0,
        }

        self.info_vars = {
            "IoT Product": self.global_config["Fuzzer"]["name"] + product["version"],
            "Target": product["type"]+"://"+product["host"]+":"+product["port"],
            "Request From Web": 0,
            "Login Status": "Login",
            "Run Time": 0,
        }

        self.results_vars = {
            "Bug Number": 0,
            "Interesting Seeds": 0,
            "Total Fuzzing Times": 0
        }

        self.gpt_vars = {
            "LLM request packages": 0,
            "LLM Code Analysis": 0
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
            level=logging.INFO,
            format="%(message)s",
            handlers=[file_handler]
        )
        self.logger = logging.getLogger('rich_logger')
        self.logger.info("[bold magenta]Logging initialized[/]")

    async def update_variables(self):
        while True:
            self.variables["SeedTemplates"] += 1
            self.variables["Seeds"] += 2
            self.variables["Variable3"] += 3
            # self.logger.info(f"[bold green]Updated variables:[/] {self.variables}")
            await asyncio.sleep(1)  # 每秒更新一次

    def render_introduction_table(self):
        # Create a table with a title and a rounded box, but without shown headers
        table = Table(title="[bold bright_yellow]" + self.global_config["Panel"]["left_top_name"] + "[/]", expand=True, box=ROUNDED, show_header=False, show_lines=False)
        # Define the columns to set their styles but hide the headers
        table.add_column("[bold green]Variable[/]", justify="left", style="cyan", no_wrap=True)
        table.add_column("[bold yellow]Value[/]", justify="left", style="bright_black", no_wrap=True)
        # Add rows from key-value pairs in self.info_vars
        for key, value in self.info_vars.items():
            table.add_row(str(key), str(value))
        
        return table
    
    def render_template_table(self):
        table = Table(title="[bold bright_yellow]"+ self.global_config["Panel"]["left_mid_name"] +"[/]", expand=True, box=ROUNDED, show_header=False, show_lines=False)
        
        # Define the columns to set their styles but hide the headers
        table.add_column("[bold green]Another Variable[/]", justify="left", style="cyan", no_wrap=True)
        table.add_column("[bold yellow]Another Value[/]", justify="left", style="magenta", no_wrap=True)
        
        for key, value in self.temlates_vars.items():
            table.add_row(str(key), str(value))
        
        return table
    
    def render_result_table(self):
        table = Table(title="[bold bright_yellow]"+ self.global_config["Panel"]["right_mid_name"] +"[/]", expand=True, box=ROUNDED, show_header=False, show_lines=False)
        
        # Define the columns to set their styles but hide the headers
        table.add_column("[bold green]Another Variable[/]", justify="left", style="cyan", no_wrap=True)
        table.add_column("[bold yellow]Another Value[/]", justify="left", style="bright_red", no_wrap=True)
        
        for key, value in self.results_vars.items():
            table.add_row(str(key), str(value))
        
        return table
    
    def render_gpt_table(self):
        table = Table(title="[bold bright_yellow]"+ self.global_config["Panel"]["right_top_name"] +"[/]", expand=True, box=ROUNDED, show_header=False, show_lines=False)
        
        # Define the columns to set their styles but hide the headers
        table.add_column("[bold green]Another Variable[/]", justify="left", style="cyan", no_wrap=True)
        table.add_column("[bold yellow]Another Value[/]", justify="left", style="bright_green", no_wrap=True)
        
        for key, value in self.gpt_vars.items():
            table.add_row(str(key), str(value))
        
        return table
    
    def format_runtime(self, elapsed_time):
        days, seconds = elapsed_time.days, elapsed_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{days} days, {hours} hrs, {minutes} min, {seconds} sec"

    async def update_runtime(self):
        elapsed_time = datetime.now() - self.start_time
        self.info_vars["Run Time"] = self.format_runtime(elapsed_time)
    
    async def display(self):
        layout = self.create_layout()
       
        with Live(layout, refresh_per_second=1, console=self.console) as live:
            while True:
                # 更新 layout 来防止重叠
                # layout = self.create_layout()
                layout["left_top_table"].update(self.render_introduction_table())
                layout["left_mid_table"].update(self.render_template_table())
                # live.update(layout)
                await self.update_runtime()
                await asyncio.sleep(0.001)


    def create_layout(self):
        layout = Layout()
        # 顶部布局
        layout.split_column(
            Layout(Panel(Align.center(self.global_config["Panel"]["panel_name"])), name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )

        # 主布局
        layout["main"].split_row(
            Layout(name="left", ratio=1),
            Layout(name="right"),
        )

        # 添加表格到左侧布局
        introduction_table = self.render_introduction_table()
        another_table = self.render_template_table()
        
        gpt_table = self.render_gpt_table()
        result_table = self.render_result_table()
        # 左侧布局的拆分，将两个表格垂直排列
        layout["left"].split_column(
            Layout(introduction_table, ratio=1, name="left_top_table"),
            Layout(another_table, ratio=1, name="left_mid_table"),
        )

        layout["right"].split_column(
            Layout(gpt_table, ratio=1, name="right_top_table"),
            Layout(result_table, ratio=2, name="right_mid_table"),
        )

        return layout
    

    
    async def run(self):
        variable_task = self.update_variables()
        display_task = self.display()
        await asyncio.gather(variable_task, display_task)

if __name__ == "__main__":
    display = RichLoggerDisplay()
    asyncio.run(display.run())