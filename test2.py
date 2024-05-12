import re

def find_variables_in_http_request(http_request):
    # 正则表达式来识别URL中的参数
    url_pattern = re.compile(r"[?&](\w+)=([^&]*)")
    # 正则表达式来识别POST数据中的参数
    post_pattern = re.compile(r"(\w+)=([^&]*)")

    # 分割请求行和头，忽略HTTP头，只关注URL和可能的POST数据
    lines = http_request.split('\n')
    request_line = lines[0]
    body = lines[-1] if len(lines) > 1 else ''

    # 检查请求类型
    method = request_line.split()[0]

    variables = {}

    # 如果是GET请求，从URL中查找参数
    if method.upper() == 'GET':
        url = request_line.split()[1]
        variables = dict(url_pattern.findall(url))

    # 如果是POST请求，从请求体中查找参数
    elif method.upper() == 'POST' and body:
        variables = dict(post_pattern.findall(body))

    return variables

# 示例HTTP请求
http_request_example = """\
GET /search?q=search+query&hl=en HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3

"""

# 或者，一个POST请求示例
http_request_example_post = """\
POST /submit HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 27

field1=value1&field2=value2
"""

# 调用函数并打印结果
print(find_variables_in_http_request(http_request_example))
print(find_variables_in_http_request(http_request_example_post))
