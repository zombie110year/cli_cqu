"""处理时间日期
"""

from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from datetime import timezone
from typing import Tuple
from ..data.schedule import HuxiSchedule, ShaPingBaSchedule
import re
import logging

__all__ = ("materialize_calendar")

# 14节 表示全天
FULL_DAY = 14


def materialize_calendar(t_week: str, t_lesson: str, start: date,
                         schedule=ShaPingBaSchedule()) -> Tuple[datetime, datetime]:
    """具体化时间日期，将一个 周次+节次 字符串转换成具体的 datetime

    例如

    >>> materialize_calendar(t_week="1", t_lesson="一[1-2节]", start=date(2020, 2, 17))
    (datetime(2019, 2, 17, 8), datetime(2017, 2, 17, 9, 40))

    比较特殊的几种编码

    1. `13节`、`14节` 表示全天

    >>> materialize_calendar(t_week="1", t_lesson="一[14节]", start=date(2020, 2, 17))
    (datetime(2019, 2, 17, 8), datetime(2017, 2, 17, 23, 59))
    """
    p_day_lesson: re.Pattern = re.compile(r"^(?P<day>[一二三四五六日])\[(?P<lesson>[\d\-]+)节\]$")
    m_day_lesson: re.Match = p_day_lesson.fullmatch(t_lesson)
    d_day_lesson: dict = m_day_lesson.groupdict()
    i_week: int = int(t_week)
    i_day: int = DAY_MAP[d_day_lesson["day"]]
    s_lesson: str = d_day_lesson["lesson"]

    if re.match(r"\d+-\d+", s_lesson):
        i_lesson: Tuple[int, int] = tuple([int(i) for i in s_lesson.split("-")])
    elif s_lesson == "14" or s_lesson == "13":
        i_lesson: int = FULL_DAY
    else:
        raise ValueError(f"{t_lesson} 无法解析课程节次")

    partial_days: int = (i_week - 1) * 7 + i_day
    if isinstance(i_lesson, tuple):
        partial_times: Tuple[timedelta, timedelta] = (schedule[i_lesson[0]][0], schedule[i_lesson[1]][1])
    elif isinstance(i_lesson, int):
        partial_times: Tuple[timedelta, timedelta] = schedule[i_lesson]
    else:
        raise TypeError(f"{i_lesson} 为 {type(i_lesson)} 类型")
    partial_td: Tuple[timedelta, timedelta] = (timedelta(days=partial_days) + partial_times[0],
                                               timedelta(days=partial_days) + partial_times[1])
    # timezone(timedelta(hours=8), "Asia/Shanghai"): 北京时间
    dt: datetime = datetime.combine(start, time.min, timezone(timedelta(hours=8), "Asia/Shanghai"))
    result = (dt + partial_td[0], dt + partial_td[1])
    return result


# 星期数的偏移量，以星期一为一周的起始
DAY_MAP = {
    "一": 0,
    "二": 1,
    "三": 2,
    "四": 3,
    "五": 4,
    "六": 5,
    "日": 6,
}
