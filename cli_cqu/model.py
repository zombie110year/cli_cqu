from pydantic import BaseModel

__all__ = ("Course", "ExperimentCourse")


class Course(BaseModel):
    "一般课程"
    # 课程号+名字
    identifier: str
    # 学分
    score: float
    # 总学时
    time_total: float
    # 教授学时
    time_teach: float
    # 上机学时
    time_practice: float
    # 类别
    classifier: str
    # 讲授方式
    teach_type: str
    # 考核方式
    exam_type: str
    # 任课教师
    teacher: str
    # 周次
    week_schedule: str
    # 节次
    day_schedule: str
    # 地点
    location: str


class ExperimentCourse(BaseModel):
    "实验课"
    # 课程号+名字
    identifier: str
    # 学分
    score: float
    # 总学时
    time_total: float
    # 教授学时
    time_teach: float
    # 上机学时
    time_practice: float
    # 项目名称
    project_name: str
    # 任课教师
    teacher: str
    # 实验值班教师
    hosting_teacher: str
    # 周次
    week_schedule: str
    # 节次
    day_schedule: str
    # 地点
    location: str
