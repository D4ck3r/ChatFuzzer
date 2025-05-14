from gpt.gpt_request import Chatbot
from generate.rawhttp_feature_extraction import split_http_request
chatbot_code = Chatbot(config_file="config.ini", chat_type="code")

while True:
    # user_input = chatbot.multi_line_input()
    user_input = chatbot_code.read_from_file()
    if user_input == '':
        continue
    if user_input.lower() == "exit":
        break
    print(chatbot_code.chat(user_input))