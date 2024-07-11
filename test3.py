import time
from rich.progress import Progress

def check_database():
    time.sleep(1)  # 模拟数据库检查延时
    return "数据库连接成功"

def check_api_service():
    time.sleep(2)  # 模拟API服务检查延时
    return "API服务可用"

def check_file_system():
    time.sleep(1.5)  # 模拟文件系统检查延时
    return "文件系统正常"

def main():
    tasks = [
        (check_database, "检查数据库"),
        (check_api_service, "检查API服务"),
        (check_file_system, "检查文件系统")
    ]

    results = []

    with Progress() as progress:
        task_progress = progress.add_task("[cyan]正在进行系统检查...", total=len(tasks))

        for task, description in tasks:
            result = task()  # 直接调用同步函数
            progress.console.print(f"{description} [bold green]完成[/]: {result}")
            progress.update(task_progress, advance=1)
            results.append(result)

        progress.console.print("[bold green]所有系统检查完成！[/]")
        print("检查结果：", results)

# 运行主函数
if __name__ == "__main__":
    main()
