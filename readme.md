
# ChatFuzz 🚀

                                                                                                                                             
                                                                                                                                             
                  ,----..     ,---,                       ___         ,---,.                                                                 
                 /   /   \  ,--.' |                     ,--.'|_     ,'  .' |                                                                 
                |   :     : |  |  :                     |  | :,'  ,---.'   |          ,--,         ,----,        ,----,              __  ,-. 
                .   |  ;. / :  :  :                     :  : ' :  |   |   .'        ,'_ /|       .'   .`|      .'   .`|            ,' ,'/ /| 
                .   ; /--`  :  |  |,--.    ,--.--.    .;__,'  /   :   :  :     .--. |  | :    .'   .'  .'   .'   .'  .'    ,---.   '  | |' | 
                ;   | ;     |  :  '   |   /       \   |  |   |    :   |  |-, ,'_ /| :  . |  ,---, '   ./  ,---, '   ./    /     \  |  |   ,' 
                |   : |     |  |   /' :  .--.  .-. |  :__,'| :    |   :  ;/| |  ' | |  . .  ;   | .'  /   ;   | .'  /    /    /  | '  :  /   
                .   | '___  '  :  | | |   \__\/: . .    '  : |__  |   |   .' |  | ' |  | |  `---' /  ;--, `---' /  ;--, .    ' / | |  | '    
                '   ; : .'| |  |  ' | :   ," .--.; |    |  | '.'| '   :  '   :  | : ;  ; |    /  /  / .`|   /  /  / .`| '   ;   /| ;  : |    
                '   | '/  : |  :  :_:,'  /  /  ,.  |    ;  :    ; |   |  |   '  :  `--'   \ ./__;     .'  ./__;     .'  '   |  / | |  , ;    
                |   :    /  |  | ,'     ;  :   .'   \   |  ,   /  |   :  \   :  ,      .-./ ;   |  .'     ;   |  .'     |   :    |  ---'     
                 \   \ .'   `--''       |  ,     .-./    ---`-'   |   | ,'    `--`----'     `---'         `---'          \   \  /            
                  `---`                  `--`---'                 `----'                                                  `----'             
                                                                                                                                             
## Description 📚

ChatFuzz is a powerful dynamic fuzz testing framework designed to identify vulnerabilities in conversational AI models. By simulating a wide range of unexpected inputs and edge cases, ChatFuzz helps detect security flaws, robustness issues, and other potential weaknesses in AI systems. The project is ideal for security researchers, AI developers, and quality assurance teams working to ensure the integrity and resilience of AI-driven chatbots and conversational agents. Built with Python, this tool integrates easily with various AI models to provide automated testing for dynamic vulnerability discovery.

## Features ✨
- **Dynamic Fuzz Testing**: ChatFuzz generates a diverse set of inputs to simulate various attack vectors, helping identify security vulnerabilities and robustness weaknesses in AI models.
- **Vulnerability Discovery**: Through dynamic analysis, the tool automatically uncovers potential vulnerabilities, such as crash-prone inputs, data leaks, and security flaws.
- **Real-Time Monitoring**: Track fuzzing activities and outcomes in real-time, with detailed logs and reports that help analyze AI behavior under unexpected conditions.
- **Highly Configurable**: Fine-tune fuzzing strategies, mutators, and test cases via configuration files, adapting the tool to different models and testing environments.
- **Session Maintenance and Device Interaction**: The tool includes mechanisms to capture and maintain session data, including login credentials and session cookies, which are crucial for testing devices or APIs that require persistent connections.

## Installation 🔧

Follow these steps to install and run ChatFuzz on your local machine:

```bash
# Run RabbitMQ (used for message queues)
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management

# Create a virtual environment
conda create --name chatfuzz-env python=3.10

# Install required dependencies
pip install -r requirements.txt

# Start the project
python main.py
```

## Configuration 🛠️

Before running ChatFuzz, you need to configure the `config.ini` file to specify API keys, test targets, and session management details:

1. **GPT API Configuration**: You will need to provide your GPT API key to enable communication with the GPT model.

   Example `config.ini` section for GPT API:
   ```ini
   [gpt_api]
   api_key = YOUR_API_KEY_HERE
   ```

2. **Test Target Configuration**: Specify the target system (API or device) for testing. Include endpoint URLs and any other relevant details.

   Example `config.ini` section for test targets:
   ```ini
   [test_target]
   target_url = https://example.com/api/v1/endpoint
   test_type = fuzzing
   ```

3. **Session Maintenance**: If your tests require login and session persistence, configure the login credentials and session cookie handling.

   Example `config.ini` section for session:
   ```ini
   [session]
   login_url = https://example.com/login
   username = your_username
   password = your_password
   session_cookie_name = session_id
   ```

## Usage 🖥️

Once the project is installed and configured, you can start using it. Here's an example of how to use it:


For command-line usage, you can run the following:

```bash
python main.py
```

This will execute the fuzzing process and output the results in the terminal. During testing, the tool will automatically handle the session and login processes as defined in `config.ini`.

### Fuzzing Results 📊

The results of each fuzzing test will be stored in the `fuzz/result` directory. This directory will contain detailed reports on the fuzzing process, including any vulnerabilities discovered and system behavior during testing. You can access the results to analyze the effectiveness of the fuzz testing and make necessary adjustments to your models.

### Screenshots 📸
Below is a screenshot of the application in action:

![alt text](<ChatFuzz.png>)

## Contributing 🤝

We welcome contributions to the project! Here's how you can help:

1. Fork the repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request to merge your changes.

Please make sure to follow the code style and include tests if possible. We appreciate all contributions!

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


## Badges 📊

Here are some badges that indicate the status of the project:

[![Build Status](https://img.shields.io/travis/username/chatfuzz.svg?style=flat-square)](https://travis-ci.org/username/chatfuzz)
[![Version](https://img.shields.io/npm/v/chatfuzz.svg?style=flat-square)](https://www.npmjs.com/package/chatfuzz)
[![License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Issues](https://img.shields.io/github/issues/username/chatfuzz.svg?style=flat-square)](https://github.com/username/chatfuzz/issues)

