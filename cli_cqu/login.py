"""读取、保存帐号密码；登录网页，获取 session
"""
from getpass import getpass
from pathlib import Path
from typing import *

import re
import time

from requests.sessions import Session

from lxml import etree
import toml

from .data.js_equality import *


class Account:
    profile = Path.home() / ".config/cli-cqu/account.toml"

    def __init_profile(self):
        if not self.profile.exists():
            if not self.profile.parent.exists():
                self.profile.parent.mkdir(parents=True)
            username = input("教学管理网帐号> ").strip()
            password = getpass("教学管理网密码> ").strip()
            print("以下是老教务网帐号，若不查成绩，则不需要登录")
            oldjw_username = input("老教务网帐号> ").strip()
            oldjw_password = getpass("老教务网密码> ").strip()

            conf = {
                "jxgl": {
                    "username": username,
                    "password": password,
                },
                "oldjw": {
                    "username": oldjw_username,
                    "password": oldjw_password
                }
            }
            with self.profile.open("wt", encoding="utf-8") as fp:
                toml.dump(conf, fp)
                print(f"配置已写入 {str(self.profile)}")

    def __init__(self):
        self.__init_profile()
        conf = toml.load(self.profile)
        self._jxgl_username = conf["jxgl"]["username"]
        self._jxgl_username = conf["jxgl"]["password"]
        self._oldjw_username = conf["oldjw"]["username"]
        self._oldjw_username = conf["oldjw"]["username"]

    def login_jxgl(self, username: str, password: str) -> Session:
        session = Session()
        session.headers.update({
            'user-agent':
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; Touch; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet PC 2.0; rv:11.0) like Gecko",
            'referer': "http://jxgl.cqu.edu.cn",
            'accept':
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.9",
            'connection': "keep-alive",
            'cache-control': "max-age=0",
            'upgrade-insecure-requests': "1",
        })

        # 初始化 Cookie
        url = f"http://jxgl.cqu.edu.cn/home.aspx"
        resp = session.get(url)
        # fix: 偶尔不需要设置 cookie, 直接就进入主页了
        # 这是跳转页 JavaScript 的等效代码
        pattern = re.compile(
            r"(?<=document.cookie=')DSafeId=([A-Z0-9]+);(?=';)")
        if pattern.search(resp.text):
            first_cookie = re.search(pattern, resp.text)[1]
            session.cookies.set("DSafeId", first_cookie)
            time.sleep(0.680)
            resp = session.get(url)
            new_cookie = resp.headers.get("set-cookie",
                                          session.cookies.get_dict())
            c = {
                1:
                re.search("(?<=ASP.NET_SessionId=)([a-zA-Z0-9]+)(?=;)",
                          new_cookie)[1],
                2:
                re.search("(?<=_D_SID=)([A-Z0-9]+)(?=;)", new_cookie)[1]
            }
            session.cookies.set("ASP.NET_SessionId", c[1])
            session.cookies.set("_D_SID", c[2])

        # 发送表单
        url = f"http://jxgl.cqu.edu.cn/_data/index_login.aspx"
        html = etree.HTML(session.get(url).text)
        login_form = {
            "__VIEWSTATE":
            html.xpath("//form[@id='Logon']/input[@name='__VIEWSTATE']")
            [0].get("value"),
            "__VIEWSTATEGENERATOR":
            html.xpath(
                "//form[@id='Logon']/input[@name='__VIEWSTATEGENERATOR']")
            [0].get("value"),
            "Sel_Type":
            "STU",
            "txt_dsdsdsdjkjkjc":
            username,  # 学号
            "txt_dsdfdfgfouyy":
            "",  # 密码, 实际上的密码加密后赋值给 efdfdfuuyyuuckjg
            "txt_ysdsdsdskgf":
            "",
            "pcInfo":
            "",
            "typeName":
            "",
            "aerererdsdxcxdfgfg":
            "",
            "efdfdfuuyyuuckjg":
            chkpwd(username, password),
        }
        page_text = session.post(
            url, data=login_form).content.decode(encoding='GBK')
        if "正在加载权限数据..." in page_text:
            return session
        if "账号或密码不正确！请重新输入。" in page_text:
            raise ValueError("账号或密码错误")
        if "该账号尚未分配角色!" in page_text:
            raise ValueError("不存在该账号")
        else:
            raise ValueError("意料之外的登陆返回页面")

    def login_oldjw(self, username: str, password: str) -> Session:
        """通过老教务网接口获取成绩单。

        登录密码和新教务网不同，如果没修改过，应为身份证后 6 位。
        """
        session = Session()
        login_form = {
            # 学号，非统一身份认证号
            "username": username,
            # 老教务网的密码和新教务不同，一般为身份证后 6 位。
            "password": password,
            # 不知道干啥的，好像也没用
            "submit1.x": 20,
            "submit1.y": 22,
            # 院系快速导航
            "select1": "#"
        }
        resp = session.post("http://oldjw.cqu.edu.cn:8088/login.asp",
                            data=login_form)
        resp_text = resp.content.decode("gbk")
        if "你的密码不正确，请到教务处咨询(学生密码错误请向学院教务人员或辅导员查询)!" in resp_text:
            raise ValueError("学号或密码错误，默认身份证后6位，或向教务处咨询")
        else:
            return session