from gpt.gpt_request import Chatbot
from generate.rawhttp_feature_extraction import split_http_request
chatbot_header = Chatbot(config_file="config.ini", chat_type="header")
chatbot_content = Chatbot(config_file="config.ini", chat_type="content")

while True:
    # user_input = chatbot.multi_line_input()
    user_input = chatbot_header.read_from_file()
    header,content = split_http_request(user_input)
    if user_input == '':
        continue
    if user_input.lower() == "exit":
        break
    print(chatbot_header.chat(header))
    if content != '':
        print(chatbot_content.chat(content))