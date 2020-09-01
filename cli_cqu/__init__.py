"""CLI CQU 是重庆大学教务系统的命令行界面
"""

import re

import json
from argparse import ArgumentParser, _SubParsersAction, Namespace
from datetime import date, datetime
from typing import *
from requests import Session
from .data.route import Parsed
from .data.schedule import New2020Schedule
from .excpetion.signal import *
from .util.calendar import make_ical
from .login import Account
__version__ = '0.4.1'

__all__ = ("App", )


def repl_parser():
    p = ArgumentParser()
    cmd = p.add_subparsers(title="command", dest="command")

    courses_json = cmd.add_parser("courses-json",
                                  description="获取本学期课程表，保存为 JSON 格式")
    courses_json.add_argument("filename", help="另存为路径（后缀 .json）")

    courses_ical = cmd.add_parser("courses-ical",
                                  description="获取本学期课程表，格式化为 ICalendar 日历")
    courses_ical.add_argument("filename", help="另存为路径（后缀 .ical）")
    courses_ical.add_argument("startdate",
                              help="yyyy-mm-dd 形式的学期开始日期，如 2020-08-31")

    assignments_json = cmd.add_parser("assignments-json", description="获取全部成绩")
    assignments_json.add_argument("filename", help="另存为路径（后缀 .json）")

    cmd_help = cmd.add_parser("help", description="显示某命令的帮助文档")
    cmd_help.add_argument("command_name",
                          help="要查看帮助的命令",
                          nargs="?",
                          default=None)

    cmd_exit = cmd.add_parser("exit", description="退出")

    return p


class App:
    def __init__(self):
        self._jxgl: Optional[Session] = None
        self._oldjw: Optional[Session] = None
        self._cmdparser = repl_parser()

    def mainloop(self):
        """命令行界面，解析指令执行对应功能"""
        while True:
            cmdline = re.split(r" +", input("cli cqu> ").strip())

            try:
                ns = self._cmdparser.parse_args(cmdline)
            except:
                continue

            self.runcmd(ns)

    def runcmd(self, ns: Namespace):
        if ns.command == "exit":
            exit()
        elif ns.command == "help":
            self.help_command(ns.command_name)
        elif ns.command == "courses-json":
            self.courses_json(ns.filename)
        elif ns.command == "courses-ical":
            self.courses_ical(ns.filename, ns.startdate)
        elif ns.command == "assignments-json":
            self.assignemnts_json(ns.filename)

    def help_command(self, command: Optional[str]):
        if command is None:
            print(self._cmdparser.format_help())
        else:
            # https://stackoverflow.com/questions/20094215/argparse-subparser-monolithic-help-output
            cmdparser = [
                action for action in self._cmdparser._actions
                if isinstance(action, _SubParsersAction)
            ][0]
            cmdaction = cmdparser.choices.get(command)
            print(cmdaction.format_help())

    def courses_json(self, filename: str):
        """选择课程表，下载为 JSON 文件"""
        courses = self._fetch_courses()
        with open(filename, "wt", encoding="utf-8") as out:
            json.dump([i.dict() for i in courses],
                      out,
                      indent=2,
                      ensure_ascii=False)

    def courses_ical(self, filename: str, startdate: str):
        "获取课程表，转化为 icalendar 格式日历日程"
        courses = self._fetch_courses()
        schedule = New2020Schedule()
        cal = make_ical(courses, date.fromisoformat(startdate), schedule)
        with open(filename, "wb") as out:
            out.write(cal.to_ical())

    def _fetch_courses(self):
        if self._jxgl is None:
            self._jxgl = Account().get_session("jxgl")

        now = datetime.now()
        # 判断学年学期，前 4 位表示学年，如 2020 表示 2020-2021 学年
        # 后 1 位为 0 或 1，分别表示第一、第二学期
        xnxq = now.year * 10 + 1 if now.month < 7 else now.year * 10
        param = {"Sel_XNXQ": xnxq, "px": 0, "rad": "on"}
        courses = Parsed.personal_courses_table(self._jxgl, param)
        return courses

    def assignemnts_json(self, filename: str):
        """从老教务网接口获取成绩单数据，保存为 JSON。

        注意，密码和新教务网不一样，默认为身份证后 6 位，所以单独使用。

        只能通过命令行参数调用。"""
        if self._oldjw is None:
            self._oldjw = Account().get_session("oldjw")
        data = Parsed.whole_assignment(self._oldjw)
        json_obj = json.dumps(data, ensure_ascii=False, indent=2)
        with open(filename, "wt", encoding="utf-8") as out:
            out.write(json_obj)


def show_help():
    print("=== help ===")
    print("""在 `cli cqu>` 提示符后输入指令

    目前提供以下指令：
    * courses-json * 获取 JSON 格式的课程表
    * courses-ical * 获取 ICalendar 日历日程格式的课程表
    * help | h | ? * 获取帮助信息
    * exit * 退出程序

    只能在命令行参数中使用的指令：
    * assignments-json * 从老教务网获取全部成绩，保存为 JSON 格式
    """)


def welcome():
    print("=== welcome ===")
    print("""欢迎使用 CLI CQU，你可以输入 help 查看帮助""")


def cli_main():
    parser = ArgumentParser("cli-cqu", description="CQU 教学管理系统的命令行界面")
    parser.add_argument("--version",
                        help="显示应用版本",
                        action="version",
                        version=f"%(prog)s {__version__}")
    args = parser.parse_args()
    app = App()
    app.mainloop()


def single_assignments_json(username, password):
    """从老教务网接口获取成绩单数据，保存为 JSON。

    注意，密码和新教务网不一样，默认为身份证后 6 位，所以单独使用。

    只能通过命令行参数调用。"""
    data = Parsed.Assignment.whole_assignment(username, password)
    json_obj = json.dumps(data, ensure_ascii=False, indent=2)

    print("=== 保存成绩单 ===")
    filename = input("保存路径（可忽略 json 扩展名）").strip()
    if not filename.endswith(".json"):
        filename = f"{filename}.json"
    with open(filename, "wt", encoding="utf-8") as out:
        out.write(json_obj)
