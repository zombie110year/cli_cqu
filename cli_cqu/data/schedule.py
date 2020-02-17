"""作息时间表
"""
from abc import abstractclassmethod
from abc import abstractmethod
from datetime import time
from typing import Tuple

__all__ = ("HuxiSchedule", "ShaPingBaSchedule")


class Schedule:
    "作息时间"

    @abstractmethod
    def get(self, index: int, default: Tuple[time, time]) -> Tuple[time, time]:
        ...

    @abstractclassmethod
    def __getitem__(cls, index: int) -> Tuple[time, time]:
        ...


class HuxiSchedule(Schedule):
    """重庆大学虎溪校区作息时间

    节次 ：（开始时间，结束时间）
    """
    __MAP__ = {
        1: (time(8, 30), time(9, 15)),
        2: (time(9, 25), time(10, 10)),
        3: (time(10, 30), time(11, 15)),
        4: (time(11, 25), time(12, 10)),
        5: (time(14), time(14, 45)),
        6: (time(14, 55), time(15, 40)),
        7: (time(16), time(16, 45)),
        8: (time(16, 55), time(17, 40)),
        9: (time(19), time(19, 45)),
        10: (time(19, 55), time(20, 40)),
        11: (time(20, 50), time(21, 35)),
        12: (time(21, 35), time(23, 59)),
    }

    def __getitem__(self, index: int) -> Tuple[time, time]:
        return self.get(index)

    @classmethod
    def get(
        cls, index: int, default=(time(8, 30), time(23, 59))
    ) -> Tuple[time, time]:
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
        1: (time(8), time(8, 45)),
        2: (time(8, 55), time(9, 40)),
        3: (time(10, 10), time(10, 55)),
        4: (time(11, 5), time(11, 50)),
        5: (time(14, 30), time(15, 15)),
        6: (time(15, 25), time(16, 10)),
        7: (time(16, 40), time(17, 25)),
        8: (time(17, 35), time(18, 20)),
        9: (time(19, 30), time(20, 15)),
        10: (time(20, 25), time(21, 10)),
        11: (time(21, 20), time(22, 5)),
        12: (time(22, 5), time(23, 59)),
    }

    def __getitem__(self, index: int) -> Tuple[time, time]:
        return self.get(index)

    @classmethod
    def get(cls, index: int, default=(time(8), time(23,
                                                    59))) -> Tuple[time, time]:
        "获取指定节次的开始、结束时间，节次在 1-12 范围之内"
        if 1 <= index <= 12:
            return cls.__MAP__[index]
        else:
            return default
