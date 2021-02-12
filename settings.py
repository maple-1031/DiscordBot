# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 00:34:55 2021

@author: maple
"""

import os
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

token = os.environ.get("DISCORD-TOKEN")
user = os.environ.get("DISCORD-USER")
password = os.environ.get("DISCORD-PASS")