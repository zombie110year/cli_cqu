"""作息时间表
"""
from abc import abstractclassmethod
from abc import abstractmethod
from datetime import timedelta
from typing import Tuple

__all__ = ("HuxiSchedule", "ShaPingBaSchedule", "New2020Schedule")


class Schedule:
    "作息时间"

    @abstractmethod
    def get(self, index: int, default: Tuple[timedelta, timedelta]) -> Tuple[timedelta, timedelta]:
        ...

    @abstractclassmethod
    def __getitem__(cls, index: int) -> Tuple[timedelta, timedelta]:
        ...


class New2020Schedule(Schedule):
    """重庆大学 2020~2021 学年起的新作息表

    节次 ：（开始时间，结束时间）
    """
    __MAP__ = {
        1: (timedelta(hours=8, minutes=30), timedelta(hours=9, minutes=15)),
        2: (timedelta(hours=9, minutes=25), timedelta(hours=10, minutes=10)),
        3: (timedelta(hours=10, minutes=30), timedelta(hours=11, minutes=15)),
        4: (timedelta(hours=11, minutes=25), timedelta(hours=12, minutes=10)),
        5: (timedelta(hours=13, minutes=30), timedelta(hours=14, minutes=15)),
        6: (timedelta(hours=14, minutes=25), timedelta(hours=15, minutes=10)),
        7: (timedelta(hours=15, minutes=20), timedelta(hours=16, minutes=5)),
        8: (timedelta(hours=16, minutes=25), timedelta(hours=17, minutes=10)),
        9: (timedelta(hours=17, minutes=20), timedelta(hours=18, minutes=5)),
        10: (timedelta(hours=19), timedelta(hours=19, minutes=45)),
        11: (timedelta(hours=19, minutes=55), timedelta(hours=20, minutes=40)),
        12: (timedelta(hours=20, minutes=50), timedelta(hours=21, minutes=35)),
    }

    def __getitem__(self, index: int) -> Tuple[timedelta, timedelta]:
        return self.get(index)

    @classmethod
    def get(
        cls, index: int, default=(timedelta(hours=8, minutes=30), timedelta(hours=23, minutes=59))
    ) -> Tuple[timedelta, timedelta]:
        "获取指定节次的开始、结束时间，节次在 1-12 范围之内"
        if 1 <= index <= 12:
            return cls.__MAP__[index]
        else:
            return default


class HuxiSchedule(Schedule):
    """重庆大学虎溪校区作息时间

    节次 ：（开始时间，结束时间）
    """
    __MAP__ = {
        1: (timedelta(hours=8, minutes=30), timedelta(hours=9, minutes=15)),
        2: (timedelta(hours=9, minutes=25), timedelta(hours=10, minutes=10)),
        3: (timedelta(hours=10, minutes=30), timedelta(hours=11, minutes=15)),
        4: (timedelta(hours=11, minutes=25), timedelta(hours=12, minutes=10)),
        5: (timedelta(hours=14), timedelta(hours=14, minutes=45)),
        6: (timedelta(hours=14, minutes=55), timedelta(hours=15, minutes=40)),
        7: (timedelta(hours=16), timedelta(hours=16, minutes=45)),
        8: (timedelta(hours=16, minutes=55), timedelta(hours=17, minutes=40)),
        9: (timedelta(hours=19), timedelta(hours=19, minutes=45)),
        10: (timedelta(hours=19, minutes=55), timedelta(hours=20, minutes=40)),
        11: (timedelta(hours=20, minutes=50), timedelta(hours=21, minutes=35)),
        12: (timedelta(hours=21, minutes=35), timedelta(hours=23, minutes=59)),
    }

    def __getitem__(self, index: int) -> Tuple[timedelta, timedelta]:
        return self.get(index)

    @classmethod
    def get(
        cls, index: int, default=(timedelta(hours=8, minutes=30), timedelta(hours=23, minutes=59))
    ) -> Tuple[timedelta, timedelta]:
        "获取指定节次的开始、结束时间，节次在 1-12 范围之内"
        if 1 <= index <= 12:
            return cls.__MAP__[index]
        else:
            return default


class ShaPingBaSchedule(Schedule):
    """沙坪坝校区作息时间

    节次 ：（开始时间，结束时间）
    """
    __MAP__ = {
        1: (timedelta(hours=8), timedelta(hours=8, minutes=45)),
        2: (timedelta(hours=8, minutes=55), timedelta(hours=9, minutes=40)),
        3: (timedelta(hours=10, minutes=10), timedelta(hours=10, minutes=55)),
        4: (timedelta(hours=11, minutes=5), timedelta(hours=11, minutes=50)),
        5: (timedelta(hours=14, minutes=30), timedelta(hours=15, minutes=15)),
        6: (timedelta(hours=15, minutes=25), timedelta(hours=16, minutes=10)),
        7: (timedelta(hours=16, minutes=40), timedelta(hours=17, minutes=25)),
        8: (timedelta(hours=17, minutes=35), timedelta(hours=18, minutes=20)),
        9: (timedelta(hours=19, minutes=30), timedelta(hours=20, minutes=15)),
        10: (timedelta(hours=20, minutes=25), timedelta(hours=21, minutes=10)),
        11: (timedelta(hours=21, minutes=20), timedelta(hours=22, minutes=5)),
        12: (timedelta(hours=22, minutes=5), timedelta(hours=23, minutes=59)),
    }

    def __getitem__(self, index: int) -> Tuple[timedelta, timedelta]:
        return self.get(index)

    @classmethod
    def get(cls, index: int, default=(timedelta(hours=8), timedelta(hours=23,
                                                                    minutes=59))) -> Tuple[timedelta, timedelta]:
        "获取指定节次的开始、结束时间，节次在 1-12 范围之内"
        if 1 <= index <= 12:
            return cls.__MAP__[index]
        else:
            return default
