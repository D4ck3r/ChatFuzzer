import asyncio
import configparser
import json
import os
import httpx
import binascii
import logging
from utils import utils

class OpenAIChatbot:
    def __init__(self, config_file='config.ini', chat_type="header", gpt_model = None):
        self.config = self.load_config(config_file)
        self.api_key = self.config['OpenAI']['api_key']
        self.endpoint = self.config['OpenAI']['endpoint']
        self.proxy = self.config['OpenAI']['proxy']
        self.gpt_config = self.config['GPT-Turbo']
        self.gpt_model = gpt_model
        if chat_type == "header":
            self.session_file_path = self.config['Session']['header_session']
            self.flag = "request"
        elif chat_type == "content":
            self.session_file_path = self.config['Session']['content_session']
            self.flag = "request"
        elif chat_type == "code":
            self.session_file_path = self.config['Session']['code_session']
            self.flag = "code"
        elif chat_type == "package_code":
            self.session_file_path = self.config['Session']['package_code_session']
            self.flag = "code"

        if self.proxy:
            self.proxies = {
                'http://': f'http://{self.proxy}',
                'https://': f'http://{self.proxy}',
            }
        else:
            self.proxies = {}
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        self.messages = self.load_messages()

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

    def load_messages(self):
        if os.path.exists(self.session_file_path):
            with open(self.session_file_path, "r") as file:
                messages = json.load(file)
        else:
            messages = [{"role": "system", "content": "You are a http protocol expert..."}]
        return messages
    
    def read_from_file(self):
        filename = input("Please enter the filename: ")  # Prompting the user for the filename in English
        try:
            with open(filename, 'rb') as file:  # Ensuring the file is read with the correct encoding
                content = file.read()  # Reading the file content as bytes
                return content.decode('utf-8')  # Decoding the bytes to string using utf-8 encoding
        except FileNotFoundError:  # Catching the case where the file does not exist
            logging.error(f"File {filename} not found.")
            return ''
        except Exception as e:  # Catching other potential exceptions
            logging.error(f"An error occurred while reading the file: {e}")
            return ''

    async def chat(self, user_input):
        if self.flag == "request":
            utils.display.gpt_vars["LLM request packages"] += 1
        elif self.flag == "code":
            utils.display.gpt_vars["LLM Code Analysis"] += 1
        
        self.tmp_messages = self.messages.copy()
        self.tmp_messages.append({"role": "user", "content": user_input})
        data = {
            "model": self.gpt_config['model'] if self.gpt_model == None else self.gpt_model,
            "messages": self.tmp_messages,
            "max_tokens": int(self.gpt_config['max_tokens']),
            "temperature": float(self.gpt_config['temperature']),
            "top_p": int(self.gpt_config['top_p']),
            "n": int(self.gpt_config['n'])
        }
        async with httpx.AsyncClient(proxies=self.proxies, timeout=10) as client:
            try:
                response = await client.post(self.endpoint, headers=self.headers, json=data)
                if response.status_code != 200:
                    logging.error(f"Failed to get valid response: Status Code {response.status_code}")
                    return 'error'
                
                try:
                    response_data = response.json()
                    response_text = response_data['choices'][0]['message']['content']
                    response_text = response_text.strip()
                    if '\r\n' not in response_text:
                        response_text = response_text.replace('\n', '\r\n')
                    response_text = response_text + '\r\n\r\n'
                    return response_text.encode("utf-8")
                except KeyError as e:
                    logging.error(f"KeyError: {e}")
                    return 'error'
                except json.JSONDecodeError as e:
                    logging.error(f"JSON decode error: {e}")
                    return 'error'
            except httpx.HTTPError as e:
                logging.error(f"GPT LLM Request error: {e}")
                return 'error'

async def main():
    chatbot = OpenAIChatbot(config_file="../config.ini", chat_type="header")
    while True:
        user_input = input("Input Your Question (Type 'exit' and press Enter to finish): ")
        if user_input.lower() == "exit":
            break
        response = await chatbot.chat(user_input)
        print(response)

if __name__ == "__main__":
    asyncio.run(main())
