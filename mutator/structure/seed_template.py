import re
import random
import aiofiles
import pickle
from utils import utils

class SeedTemplate:
    def __init__(self, priority, map_id):
        self.header_marked_fields = []
        self.header_unmarked_fields = []
        self.header_mutate_array = []
        self.content_marked_fields = []
        self.content_unmarked_fields = []
        self.content_mutate_array = []
        self.mutation_dict = {"header":[],"content":[]}
        # self.send_header = None
        # self.send_content = None
        self.id = None
        self.parent_id = None
        self.child_dict = {}
        self.label_head = ''
        self.label_content = ''
        self.priority = priority
        self.map_id = map_id
        self.success = 100
        self.failed = 100
        self.response = []
        self.times = 0

    def is_type(self, s):
        if re.match(rb'^[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?$', s.strip()):
            return "num"
        else:
            return "str"

    def set_id(self, id):
        self.id = id
        
    def extract_and_separate_fields(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        pattern = re.compile(rb'\$#(.*?)#\$')
        fields = re.split(pattern, data)
        marked_fields = [[f, self.is_type(f),0] for i, f in enumerate(fields) if i % 2 != 0]
        unmarked_fields = [f for i, f in enumerate(fields) if i % 2 == 0]
        return marked_fields, unmarked_fields

    def set_label_header(self, label_head):
        self.label_head = label_head
        self.header_marked_fields, self.header_unmarked_fields = self.extract_and_separate_fields(label_head)
    
    def set_label_content(self, label_content):
        self.label_content = label_content
        self.content_marked_fields, self.content_unmarked_fields = self.extract_and_separate_fields(label_content)
    
    def set_header_mutate_array(self):
        self.header_mutate_array = [ item for item in range(len(self.header_marked_fields))]

    def set_content_mutate_array(self):
        self.content_mutate_array = [ item for item in range(len(self.content_marked_fields))]

    # def set_send_header(self, send_header):
    #     self.send_header = send_header

    # def set_send_content(self, send_content):
    #     self.send_content = send_content

    def reconstruct_packet(self):
        reconstructed_packet = b""
        for unmarked, (marked, type_, num_) in zip(self.header_unmarked_fields, self.header_marked_fields):
            reconstructed_packet += unmarked + marked
        if len(self.header_unmarked_fields) > len(self.header_marked_fields):
            reconstructed_packet += self.header_unmarked_fields[-1]

        # reconstructed_packet += b"\r\n"
        content_packet = b""
        for unmarked, (marked, type_, num_) in zip(self.content_unmarked_fields, self.content_marked_fields):
            content_packet += unmarked + marked
        if len(self.content_unmarked_fields) > len(self.content_marked_fields):
            content_packet += self.content_unmarked_fields[-1]

        content_length = len(content_packet)
        reconstructed_packet = self.update_content_length(reconstructed_packet, content_length)
        reconstructed_packet += content_packet
        
        return reconstructed_packet
    
    def update_content_length(self, header: bytes, new_length: int) -> bytes:
        pattern = re.compile(rb'(?<=Content-Length: )\d+(?=\r\n)')
        # 将新的内容长度转换为字节串
        replacement = str(new_length).encode('utf-8')
        # 使用正则表达式进行替换
        updated_header = re.sub(pattern, replacement, header)
        return updated_header
    
    def renew_object(self, index, ftype):
        if ftype == "header":
            self.header_mutate_array.remove(index)
        elif ftype == "content":
            self.content_mutate_array.remove(index)

    def __lt__(self, other):
            return self.priority < other.priority
    
    async def save_to_file(self, filename, response=b"NULL", mutation={"id": '', "package": '', "index": -1, "mutation": b'NULL'}):
        async with aiofiles.open(filename, 'wb') as output_file:
            await output_file.write(pickle.dumps(self))
        
        if utils.global_config["Fuzzer"]["model"] == "DEBUG":
            async with aiofiles.open(filename+'-response', 'wb') as output_file:
                await output_file.write(response)
            async with aiofiles.open(filename+'-mutation', 'wb') as output_file:
                await output_file.write(mutation["mutation"])
            async with aiofiles.open(filename+'-index', 'w') as output_file:
                await output_file.write(str(mutation["index"]))

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'rb') as input_file:
            return pickle.load(input_file)
    
    def sample_beta(self):
        return random.betavariate(self.success + 1, self.failed + 1)

if __name__ == "__main__":
    head = b"""
POST /login/Auth HTTP/1.1\r
Host: 192.168.0.200\r
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:$#125.0#$) Gecko/20100101 Firefox/$#125.0#$\r
Accept: */*\r
Accept-Language: en-US,en;q=$#0.5#$\r
Accept-Encoding: gzip, deflate\r
Content-Type: application/x-www-form-urlencoded; charset=$#UTF-8#$\r
X-Requested-With: XMLHttpRequest\r
Content-Length: $#56#$\r
Origin: http://$#192.168.0.200#$\r
Connection: close\r
Referer: http://192.168.0.200/login.html\r
Cookie: password=$#7da188c2e2d83e38b7d9e75e500f1af8eqp5gk#$\r
"""
    
    content = b"ddddd=$#asdf#$"
    st = SeedTemplate(1, "xx")
    st.set_label_header(head)
    st.set_label_content(content)
    print(st.header_marked_fields)
    print(st.content_marked_fields)
    st.content_marked_fields[0][0] = b"++++++++++++++++"
    print(st.reconstruct_packet())
