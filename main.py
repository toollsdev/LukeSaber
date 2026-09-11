# -*- coding: utf-8 -*-
from platform import python_version

from utils.client import BotPool

print("Luke's Saber | toollsdev | https://github.com/toollsdev/lukesaber")
print(f"🐍 - Versão do python: {python_version()}")

pool = BotPool()

pool.setup()
