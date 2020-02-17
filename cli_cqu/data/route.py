"""jxgl.cqu.edu.cn 网址的路由
"""
import logging
from typing import List
from typing import Union

from bs4 import BeautifulSoup
from requests import Session

from ..model import Course
from ..model import ExperinceCourse
from . import HOST

__all__ = ("Route", "Parsed")


class Route:
    home = "/home.aspx"
    mainform = "/MAINFRM.aspx"

    class TeachingArragement:
        "教学安排模块"
        # 个人课表
        personal_cources = "/znpk/Pri_StuSel.aspx"
        # 查询个人课表
        personal_cources_table = "/znpk/Pri_StuSel_rpt.aspx"


class Parsed:
    class TeachingArragement:
        "教学安排模块"

        # todo: 只使用 get 方法
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
                el_排序 = html.select("select[name=px] > option")
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
                logging.error("你应当将表单提交到 /znpk/Pri_StuSel_rpt.aspx")
                return {"error": "should post to /znpk/Pri_StuSel_rpt.aspx"}
            else:
                return {"raw": s.request(method, url)}

        @staticmethod
        def personal_cources_table(
                s: Session,
                data: dict) -> List[Union[Course, ExperinceCourse]]:
            """查询个人课表，需要的表单信息可以通过
            Route.TeachingArrangement.personal_cources 获取
            """
            url = f"{HOST.PREFIX}{Route.TeachingArragement.personal_cources_table}"
            resp = s.post(url, data=data)
            html = BeautifulSoup(resp.text, "lxml")
            listing = html.select("table > tbody > tr")
            cources = [make_course(i) for i in listing]
            return cources


def makeurl(path: str) -> str:
    "将 path 补全为完整的 url"
    return f"{HOST.PREFIX}{path}"


def make_course(tr: BeautifulSoup) -> Union[Course, ExperinceCourse]:
    "根据传入的 tr 元素，获取对应的 Course 对象"
    td = tr.select("td")
    # 第一列是序号，忽略
    if len(td) == 13:
        return Course(
            identifier=td[1].text
            if td[1].text != "" else td[1].attrs["hidevalue"],
            score=float(
                td[2].text if td[2].text != "" else td[2].attrs["hidevalue"]),
            time_total=float(
                td[3].text if td[3].text != "" else td[3].attrs["hidevalue"]),
            time_teach=float(
                td[4].text if td[4].text != "" else td[4].attrs["hidevalue"]),
            time_practice=float(
                td[5].text if td[5].text != "" else td[5].attrs["hidevalue"]),
            classifier=td[6].text
            if td[6].text != "" else td[6].attrs["hidevalue"],
            teach_type=td[7].text
            if td[7].text != "" else td[7].attrs["hidevalue"],
            exam_type=td[8].text
            if td[8].text != "" else td[8].attrs["hidevalue"],
            teacher=td[9].text
            if td[9].text != "" else td[9].attrs["hidevalue"],
            week_schedule=td[10].text,
            day_schedule=td[11].text,
            location=td[12].text)
    elif len(td) == 12:
        return ExperinceCourse(
            identifier=td[1].text
            if td[1].text != "" else td[1].attrs["hidevalue"],
            score=float(
                td[2].text if td[2].text != "" else td[2].attrs["hidevalue"]),
            time_total=float(
                td[3].text if td[3].text != "" else td[3].attrs["hidevalue"]),
            time_teach=float(
                td[4].text if td[4].text != "" else td[4].attrs["hidevalue"]),
            time_practice=float(
                td[5].text if td[5].text != "" else td[5].attrs["hidevalue"]),
            project_name=td[6].text
            if td[6].text != "" else td[6].attrs["hidevalue"],
            teacher=td[7].text
            if td[7].text != "" else td[7].attrs["hidevalue"],
            hosting_teacher=td[8].text
            if td[8].text != "" else td[8].attrs["hidevalue"],
            week_schedule=td[9].text
            if td[9].text != "" else td[9].attrs["hidevalue"],
            day_schedule=td[10].text
            if td[10].text != "" else td[10].attrs["hidevalue"],
            location=td[11].text
            if td[11].text != "" else td[11].attrs["hidevalue"],
        )
    else:
        logging.error("未知的数据结构")
        logging.error(tr.prettify())
        raise ValueError("未知的数据结构")
