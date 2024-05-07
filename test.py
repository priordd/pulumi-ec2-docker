import myshellscript

user_data = """#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt install docker.io -y
"""

user_data = user_data + myshellscript.custom
print(user_data)
