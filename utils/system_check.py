import time
import os 
from rich.progress import Progress
from mutator.structure.seed_template import SeedTemplate
from utils import utils
import pika
import sys

class SystemChecker:
    def __init__(self):
        self.tasks = [
            (self.check_rabbitmq, "Check RabbitMQ Connect"),
            (self.check_gpt_api, "Check GPT API"),
            (self.check_file_system, "Check File System"),
            (self.check_template_dir, "Check & Load Seed Template DIR")
        ]
        self.config = utils.global_config


    def check_rabbitmq(self):
        connection_params = pika.URLParameters(self.config['RabbitMQ']['url'])
        try:
            connection = pika.BlockingConnection(connection_params)
            if connection.is_open:
                connection.close()
                return "RabbitMQ Connect Success"
            else:
                return "RabbitMQ Connection Failed"
        except Exception  as e:
            return f"RabbitMQ Connection Failed: {e}"
        
    def check_gpt_api(self):
        time.sleep(2)  # 模拟API服务检查延时
        return "GPT API-KEY Avaliable"

    def check_file_system(self):
        time.sleep(1.5)  # 模拟文件系统检查延时
        return "File System Writable"

    def check_template_dir(self):
        # templates = []
        for filename in os.listdir(utils.global_config["Fuzzer"]["debug_dir_template"]):
            full_path = os.path.join(utils.global_config["Fuzzer"]["debug_dir_template"], filename)
            template: SeedTemplate = SeedTemplate.load_from_file(full_path)
            utils.root_tp_dict[template.id] = template
            utils.all_tp_dict[template.id] = template
            utils.display.template_num += 1
        return "Seed Template Load Success"

    def run_checks(self):
        results = []

        with Progress() as progress:
            task_progress = progress.add_task("[cyan]Checking System...", total=len(self.tasks))

            for task, description in self.tasks:
                result = task()  # 直接调用同步函数
                if "failed" in result.lower():
                    progress.console.print(f"{description} [bold red]Failed![/]: {result}")
                    sys.exit()
                progress.console.print(f"{description} [bold green]Done![/]: {result}")
                progress.update(task_progress, advance=1)
                results.append(result)

            progress.console.print("[bold green]ALL Done！[/]")
        return results

def main():
    checker = SystemChecker()
    results = checker.run_checks()
    print("检查结果：", results)

# 运行主函数
if __name__ == "__main__":
    main()
