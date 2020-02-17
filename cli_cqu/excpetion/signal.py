__all__ = ("Signal", "SigContinue", "SigExit", "SigDone", "SigHelp")


class Signal(Exception):
    pass


class SigContinue(Exception):
    "指示：继续"
    pass


class SigExit(Exception):
    "指示：退出"
    pass


class SigDone(SigContinue):
    "指示：完成当前任务"
    pass


class SigHelp(SigContinue):
    "指示：提供帮助"
    pass
