from gpt.gpt_request import Chatbot
from generate.rawhttp_feature_extraction import split_http_request
import asyncio

chatbot_vul = Chatbot(config_file="config.ini", chat_type="vul", api_key_prefix= 'DeepSeek')

async def interact_with_chatbot():
    while True:
        user_input = chatbot_vul.multi_line_input()
        # user_input = chatbot_vul.read_from_file()
        if user_input == '':
            continue
        if user_input.lower() == "exit":
            break
        response_header = await chatbot_vul.chat(user_input)  # 异步调用chat方法
        print(response_header)
        # print(response_header.decode('utf-8'))  # 打印返回的响应


if __name__ == "__main__":
    asyncio.run(interact_with_chatbot())
