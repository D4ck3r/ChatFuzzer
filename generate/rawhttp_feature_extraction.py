import re

from utils.utils import calculate_md5


def split_http_request(http_request):
    parts = http_request.split("\r\n\r\n", 1)
    header = parts[0]
    content = parts[1] if len(parts) > 1 else ''
    return header, content

def head_one_line(head):
    lines = head.split('\r\n')
    start_line = lines[0]
    return start_line

def remove_blank(content):
    return re.sub(r'[\s\r\n\t]+', '', content)

def remove_random(content):
    pattern = r'\b(?=\w*\d)[A-Za-z0-9.-_]{3,}\b'
    cleaned_text = re.sub(pattern, '', content)
    return cleaned_text

def check_statics(header_one):
    parts = header_one.split()
    if len(parts) < 2:
        return False

    url_path = parts[1].split('?')[0]

    static_extensions = [
        '.jpg', '.jpeg', '.png', '.gif', '.css', '.js',
        '.ico', '.svg', '.webp', '.mp3', '.mp4', '.woff',
        '.woff2', '.ttf', '.eot', '.otf', '.json'
    ]
    return any(url_path.lower().endswith(ext) for ext in static_extensions)

def extract_host(content):
    host_pattern = re.compile(r'Host:\s*(.*)', re.IGNORECASE)
    match = host_pattern.search(content)
    if match:
        return match.group(1).strip()
    return None

def feature_extraction(content):
    header, content = split_http_request(content)
    header_one = head_one_line(header)
    flag = check_statics(header_one)
    merge = header_one + content
    res = remove_random(merge)
    res = remove_blank(res)
    host = extract_host(content)
    # print(res)
    return calculate_md5(res),res,flag,{"header": header, "content": content},host

if __name__ == '__main__':
    feature_extraction("en=user_engagement&_et=1209&en=page_view&_ee=1&ep.version=6.6.1&ep.build=90&ep.model=Cisco%20Firepower%20Management%20Center%20for%20VMWare&ep.appliance_id=6ee7825b0ebc9ab0aefaf45c1c5583f466312c9f2c7955a7d376e6e45dd4d1d4&ep.theme=light&dt=Cisco%20Firepower%20Management%20Center%20for%20VMWare%206.6.1-90&dp=%2Fui%2Flogin")
    # print(feature_extraction("asdf"))
    # print(feature_extraction())