import time
from rich.progress import Progress

class SystemChecker:
    def __init__(self):
        self.tasks = [
            (self.check_rabbitmq, "Check RabbitMQ Connect"),
            (self.check_gpt_api, "Check GPT API"),
            (self.check_file_system, "Check File System")
        ]

    def check_rabbitmq(self):
        time.sleep(1)  
        return "RabbitMQ Connect Success"

    def check_gpt_api(self):
        time.sleep(2)  # 模拟API服务检查延时
        return "GPT API-KEY Avaliable"

    def check_file_system(self):
        time.sleep(1.5)  # 模拟文件系统检查延时
        return "File System Writable"

    def run_checks(self):
        results = []

        with Progress() as progress:
            task_progress = progress.add_task("[cyan]Checking System...", total=len(self.tasks))

            for task, description in self.tasks:
                result = task()  # 直接调用同步函数
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
