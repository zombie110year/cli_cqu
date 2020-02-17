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
# 帮助信息
info = Parsed.TeachingArragement.personal_cources(app.session)
pprint(info)


print("=== 表单自动构建，请提供选项 ===")
xnxq_list = info["Sel_XNXQ"]
for i, li in enumerate(xnxq_list):
    print(f"{i}: {li['text']}")

xnxq_i = int(input("学年学期[0|1]> ").rstrip())
xnxq = info["Sel_XNXQ"][xnxq_i]["value"]

param = {"Sel_XNXQ": xnxq, "px": 0, "rad": "on"}
table = Parsed.TeachingArragement.personal_cources_table(app.session, param)

pprint(table)

with open("result.json", "wt", encoding="utf-8") as out:
    json.dump([i.dict() for i in table], out, indent=2, ensure_ascii=False)
