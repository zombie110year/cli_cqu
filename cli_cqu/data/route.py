"""jxgl.cqu.edu.cn 网址的路由
"""
import logging
from typing import List
from typing import Union

from bs4 import BeautifulSoup
from requests import Session

from ..model import Course
from ..model import ExperimentCourse
from . import HOST

__all__ = ("Route", "Parsed")


class Route:
    home = "/home.aspx"
    mainform = "/MAINFRM.aspx"

    class TeachingArrangement:
        "教学安排模块"
        # 个人课表
        personal_courses = "/znpk/Pri_StuSel.aspx"
        # 查询个人课表
        personal_courses_table = "/znpk/Pri_StuSel_rpt.aspx"

    #TODO: 开学后连内网才能连接老教务网
    class Assignment:
        """成绩单

        为了避开因未评教而拒绝提供成绩单查询的行为，通过老教务网接口获取数据。
        """
        oldjw_login = "http://oldjw.cqu.edu.cn:8088/"
        # 全部成绩
        whole_assignment = "http://oldjw.cqu.edu.cn:8088/score/sel_score/sum_score_sel.asp"


class Parsed:
    class TeachingArrangement:
        "教学安排模块"

        @staticmethod
        def personal_courses(s: Session) -> dict:
            "解析个人课表页面，获取可得的信息"
            url = f"{HOST.PREFIX}{Route.TeachingArrangement.personal_courses}"
            # 需要填写的表单数据以及说明
            resp = s.get(url)
            html = BeautifulSoup(resp.text, "lxml")
            el_学年学期 = html.select("select[name=Sel_XNXQ] > option")
            学年学期 = [{"text": i.text, "value": int(i.attrs["value"])} for i in el_学年学期]
            el_排序 = html.select("select[name=px] > option")
            return {"Sel_XNXQ": 学年学期, "rad": {"text": "总是 on，不知道干嘛的", "value": "on"}, "###": "始终全量获取"}

        @staticmethod
        def personal_courses_table(s: Session, data: dict) -> List[Union[Course, ExperimentCourse]]:
            """查询个人课表，需要的表单信息可以通过
            Route.TeachingArrangement.personal_courses 获取
            """
            url = f"{HOST.PREFIX}{Route.TeachingArrangement.personal_courses_table}"
            resp = s.post(url, data=data)
            html = BeautifulSoup(resp.text, "lxml")
            listing = html.select("table > tbody > tr")
            courses = [make_course(i) for i in listing]
            return courses

    class Assignment:
        @staticmethod
        def whole_assignment() -> List[Tuple[None]]:
            pass


def makeurl(path: str) -> str:
    "将 path 补全为完整的 url"
    return f"{HOST.PREFIX}{path}"


def make_course(tr: BeautifulSoup) -> Union[Course, ExperimentCourse]:
    "根据传入的 tr 元素，获取对应的 Course 对象"
    td = tr.select("td")
    # 第一列是序号，忽略
    if len(td) == 13:
        return Course(identifier=td[1].text if td[1].text != "" else td[1].attrs.get("hidevalue", ''),
                      score=float(td[2].text if td[2].text != "" else td[2].attrs.get("hidevalue", '')),
                      time_total=float(td[3].text if td[3].text != "" else td[3].attrs.get("hidevalue", '')),
                      time_teach=float(td[4].text if td[4].text != "" else td[4].attrs.get("hidevalue", '')),
                      time_practice=float(td[5].text if td[5].text != "" else td[5].attrs.get("hidevalue", '')),
                      classifier=td[6].text if td[6].text != "" else td[6].attrs.get("hidevalue", ''),
                      teach_type=td[7].text if td[7].text != "" else td[7].attrs.get("hidevalue", ''),
                      exam_type=td[8].text if td[8].text != "" else td[8].attrs.get("hidevalue", ''),
                      teacher=td[9].text if td[9].text != "" else td[9].attrs.get("hidevalue", ''),
                      week_schedule=td[10].text,
                      day_schedule=td[11].text,
                      location=td[12].text)
    elif len(td) == 12:
        return ExperimentCourse(
            identifier=td[1].text if td[1].text != "" else td[1].attrs.get("hidevalue", ''),
            score=float(td[2].text if td[2].text != "" else td[2].attrs.get("hidevalue", '')),
            time_total=float(td[3].text if td[3].text != "" else td[3].attrs.get("hidevalue", '')),
            time_teach=float(td[4].text if td[4].text != "" else td[4].attrs.get("hidevalue", '')),
            time_practice=float(td[5].text if td[5].text != "" else td[5].attrs.get("hidevalue", '')),
            project_name=td[6].text if td[6].text != "" else td[6].attrs.get("hidevalue", ''),
            teacher=td[7].text if td[7].text != "" else td[7].attrs.get("hidevalue", ''),
            hosting_teacher=td[8].text if td[8].text != "" else td[8].attrs.get("hidevalue", ''),
            week_schedule=td[9].text if td[9].text != "" else td[9].attrs.get("hidevalue", ''),
            day_schedule=td[10].text if td[10].text != "" else td[10].attrs.get("hidevalue", ''),
            location=td[11].text if td[11].text != "" else td[11].attrs.get("hidevalue", ''),
        )
    else:
        logging.error("未知的数据结构")
        logging.error(tr.prettify())
        raise ValueError("未知的数据结构")
