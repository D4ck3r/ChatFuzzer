import socket

def send_http_request():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.200', 80))
    request_header = (
        'POST /login/Auth HTTP/1.1\r\n'
        'Host: 192.168.0.200\r\n'
        'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0\r\n'
        'Accept: */*\r\n'
        'Accept-Language: en-US,en;q=0.5\r\n'
        'Accept-Encoding: gzip, deflate\r\n'
        'Content-Type: application/x-www-form-urlencoded; charset=UTF-8\r\n'
        'X-Requested-With: XMLHttpRequest\r\n'
        'Content-Length: 56\r\n'
        'Origin: http://192.168.0.200\r\n'
        'Connection: close\r\n'
        'Referer: http://192.168.0.200/login.html\r\n'
        'Cookie: password=7da188c2e2d83e38b7d9e75e500f1af8rnp5gk\r\n'
        '\r\n'
        'username=admin&password=7da188c2e2d83e38b7d9e75e500f1af8'
    )
    
    s.sendall(request_header.encode())

    response = b''
    while True:
        part = s.recv(1024)
        if not part:
            break
        response += part

    # s.close()
    print(response.decode())
   
    return response.decode()

send_http_request()
