"""下载课程表
"""
import json
from pathlib import Path
from pprint import pprint
from sys import path

path.append(str(Path(__file__).parent.parent.absolute()))

from cli_cqu import App
from cli_cqu.data.route import Parsed

# 登录
app = App()
app.courses_table()
