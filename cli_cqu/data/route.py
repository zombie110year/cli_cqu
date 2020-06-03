"""jxgl.cqu.edu.cn 网址的路由
"""
import logging
import re
from typing import *

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

    class Assignment:
        """成绩单

        为了避开因未评教而拒绝提供成绩单查询的行为，通过老教务网接口获取数据。
        """
        # 发送 POST 获取会话
        oldjw_login = "http://oldjw.cqu.edu.cn:8088/login.asp"
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
            学年学期 = [{
                "text": i.text,
                "value": int(i.attrs["value"])
            } for i in el_学年学期]
            el_排序 = html.select("select[name=px] > option")
            return {
                "Sel_XNXQ": 学年学期,
                "rad": {
                    "text": "总是 on，不知道干嘛的",
                    "value": "on"
                },
                "###": "始终全量获取"
            }

        @staticmethod
        def personal_courses_table(
                s: Session,
                data: dict) -> List[Union[Course, ExperimentCourse]]:
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
        def whole_assignment(u: str, p: str) -> dict:
            """通过老教务网接口获取成绩单。

            登录密码和新教务网不同，如果没修改过，应为身份证后 6 位。

            :param str u: 学号
            :param str p: 登录密码

            包含字段::

                学号（str）
                姓名（str）
                专业（str）
                GPA（str）
                查询时间（str）
                详细（List[dict]）
                    课程编码（str）
                    课程名称（str）
                    成绩（str）
                    学分（str）
                    选修（str）
                    类别（str）
                    教师（str）
                    考别（str）
                    备注（str）
                    时间（str）
            """
            login_form = {
                # 学号，非统一身份认证号
                "username": u,
                # 老教务网的密码和新教务不同，一般为身份证后 6 位。
                "password": p,
                # 不知道干啥的，好像也没用
                "submit1.x": 20,
                "submit1.y": 22,
                # 院系快速导航
                "select1": "#"
            }
            session = Session()
            resp = session.post(Route.Assignment.oldjw_login, data=login_form)
            resp_text = resp.content.decode("gbk")
            if "你的密码不正确，请到教务处咨询(学生密码错误请向学院教务人员或辅导员查询)!" in resp_text:
                raise ValueError("学号或密码错误，老教务处的密码默认为身份证后六位，"
                                 #
                                 "或到教务处咨询(学生密码错误请向学院教务人员或辅导员查询)!")

            assignments = session.get(
                Route.Assignment.whole_assignment).content.decode("gbk")
            assparse = BeautifulSoup(assignments, "lxml")

            header_text = str(assparse.select_one("td > p:nth-child(2)"))
            header = [
                t for t in (re.sub(r"</b>|</?p>|\s", "", t)
                            for t in header_text.split("<b>")) if t != ""
            ]

            details = []
            for tr in assparse.select("tr")[3:-1]:
                tds = [re.sub(r"\s", "", td.text) for td in tr.select("td")]
                data = {
                    "课程编码": tds[1],
                    "课程名称": tds[2],
                    "成绩": tds[3],
                    "学分": tds[4],
                    "选修": tds[5],
                    "类别": tds[6],
                    "教师": tds[7],
                    "考别": tds[8],
                    "备注": tds[9],
                    "时间": tds[10],
                }
                details.append(data)

            查询时间 = re.search(
                r"查询时间：(2\d{3}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})",
                assignments)
            table = {
                "学号": header[0][3:],
                "姓名": header[1][3:],
                "专业": header[2][3:],
                "GPA": header[3][4:],
                "查询时间": 查询时间[1] if 查询时间 is not None else "Unknown",
                "详细": details,
            }
            return table


def makeurl(path: str) -> str:
    "将 path 补全为完整的 url"
    return f"{HOST.PREFIX}{path}"


def make_course(tr: BeautifulSoup) -> Union[Course, ExperimentCourse]:
    "根据传入的 tr 元素，获取对应的 Course 对象"
    td = tr.select("td")
    # 第一列是序号，忽略
    if len(td) == 13:
        return Course(
            identifier=td[1].text if td[1].text != "" else td[1].attrs.get(
                "hidevalue", ''),
            score=float(td[2].text if td[2].text != "" else td[2].attrs.
                        get("hidevalue", '')),
            time_total=float(td[3].text if td[3].text != "" else td[3].attrs.
                             get("hidevalue", '')),
            time_teach=float(td[4].text if td[4].text != "" else td[4].attrs.
                             get("hidevalue", '')),
            time_practice=float(td[5].text if td[5].text != "" else td[5].
                                attrs.get("hidevalue", '')),
            classifier=td[6].text if td[6].text != "" else td[6].attrs.get(
                "hidevalue", ''),
            teach_type=td[7].text if td[7].text != "" else td[7].attrs.get(
                "hidevalue", ''),
            exam_type=td[8].text if td[8].text != "" else td[8].attrs.get(
                "hidevalue", ''),
            teacher=td[9].text if td[9].text != "" else td[9].attrs.get(
                "hidevalue", ''),
            week_schedule=td[10].text,
            day_schedule=td[11].text,
            location=td[12].text)
    elif len(td) == 12:
        return ExperimentCourse(
            identifier=td[1].text if td[1].text != "" else td[1].attrs.get(
                "hidevalue", ''),
            score=float(td[2].text if td[2].text != "" else td[2].attrs.
                        get("hidevalue", '')),
            time_total=float(td[3].text if td[3].text != "" else td[3].attrs.
                             get("hidevalue", '')),
            time_teach=float(td[4].text if td[4].text != "" else td[4].attrs.
                             get("hidevalue", '')),
            time_practice=float(td[5].text if td[5].text != "" else td[5].
                                attrs.get("hidevalue", '')),
            project_name=td[6].text if td[6].text != "" else td[6].attrs.get(
                "hidevalue", ''),
            teacher=td[7].text if td[7].text != "" else td[7].attrs.get(
                "hidevalue", ''),
            hosting_teacher=td[8].text
            if td[8].text != "" else td[8].attrs.get("hidevalue", ''),
            week_schedule=td[9].text if td[9].text != "" else td[9].attrs.get(
                "hidevalue", ''),
            day_schedule=td[10].text
            if td[10].text != "" else td[10].attrs.get("hidevalue", ''),
            location=td[11].text if td[11].text != "" else td[11].attrs.get(
                "hidevalue", ''),
        )
    else:
        logging.error("未知的数据结构")
        logging.error(tr.prettify())
        raise ValueError("未知的数据结构")
