"""jxgl.cqu.edu.cn 网址的路由
"""
from requests import Session
from bs4 import BeautifulSoup
from . import HOST

__all__ = ("Route", "Parsed")


class Route:
    home = "/home.aspx"
    mainform = "/MAINFRM.aspx"

    class TeachingArragement:
        "教学安排模块"
        # 个人课表
        personal_cources = "/znpk/Pri_StuSel.aspx"


class Parsed:
    class TeachingArragement:
        "教学安排模块"

        @staticmethod
        def personal_cources(s: Session,
                             method="get",
                             data: dict = None) -> dict:
            "解析个人课表页面，获取可得的信息"
            method = method.lower()
            url = f"{HOST.PREFIX}{Route.TeachingArragement.personal_cources}"
            if method == "get":
                # 需要填写的表单数据以及说明
                resp = s.request(method, url)
                html = BeautifulSoup(resp.text, "lxml")
                el_学年学期 = html.select("select[name=Sel_XNXQ] > option")
                学年学期 = [{
                    "text": i.text,
                    "value": i.attrs["value"]
                } for i in el_学年学期]
                el_是否选择周次 = html.select_one("input[name=zc_flag]")
                el_设定周次 = html.select("input[name=zc_input]")
                是否周次 = {"text": "周次", "value": el_是否选择周次.attrs["value"]}
                周次 = [{
                    "text": i.text,
                    "value": i.attrs["value"]
                } for i in el_设定周次]
                el_排序 = html.select("select[name=px] > input")
                排序 = [{
                    "text": i.text,
                    "value": i.attrs["value"]
                } for i in el_排序]

                return {
                    "Sel_XNXQ": 学年学期,
                    "zc_flag": 是否周次,
                    "zc_input": 周次,
                    "px": 排序,
                    "rad": {
                        "text": "总是 on，不知道干嘛的",
                        "value": "on"
                    },
                    "###": "当 zc_flag 为 0 时，可以不传入 zc_* 两个参数"
                }

            elif method == "post":
                # 提交表单，查询课表
                resp = s.request(method, url, data=data)
            else:
                return {"raw": s.request(method, url)}


def makeurl(path: str) -> str:
    "将 path 补全为完整的 url"
    return f"{HOST.PREFIX}{path}"
