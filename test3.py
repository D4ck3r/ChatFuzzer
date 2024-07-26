import psutil

def count_connections(port):
    count = 0
    connections = psutil.net_connections(kind='inet')
    for conn in connections:
        if conn.laddr.port == port and conn.status == 'ESTABLISHED':
            count += 1
    return count

# 示例：监控端口8080的活动连接数
port = 8080
active_connections = count_connections(port)
print(f"Active connections on port {port}: {active_connections}")
