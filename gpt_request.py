import asyncio
import configparser
import json
import os
import httpx
import binascii
import logging

class OpenAIChatbot:
    def __init__(self, config_file='config.ini', chat_type="header"):
        self.config = self.load_config(config_file)
        self.api_key = self.config['OpenAI']['api_key']
        self.endpoint = self.config['OpenAI']['endpoint']
        self.proxy = self.config['OpenAI']['proxy']
        self.gpt_config = self.config['GPT-Turbo']
        
        if chat_type == "header":
            self.session_file_path = self.config['Session']['header_session']
        elif chat_type == "content":
            self.session_file_path = self.config['Session']['content_session']
        if self.proxy != "":
            self.proxies = {
                'http://': f'http://{self.proxy}',
                'https://': f'http://{self.proxy}',
            }
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

    async def chat(self, user_input):
        self.tmp_messages = self.messages.copy()
        self.tmp_messages.append({"role": "user", "content": user_input})
        data = {
            "model": self.gpt_config['model'],
            "messages": self.tmp_messages,
            "max_tokens": int(self.gpt_config['max_tokens']),
            "temperature": float(self.gpt_config['temperature']),
            "top_p": int(self.gpt_config['top_p']),
            "n": int(self.gpt_config['n'])
        }
        async with httpx.AsyncClient(proxies=self.proxies) as client:
            try:
                response = await client.post(self.endpoint, headers=self.headers, json=data)
                if response.status_code == 429:
                    return 'error'
                response_text = response.json()['choices'][0]['message']['content']
                # print(response.content)
                response_text = response_text.strip()
                if '\r\n' not in response_text:
                    response_text = response_text.replace('\n', '\r\n')
                response_text = response_text + '\r\n\r\n'
                return response_text.encode("utf-8")
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
