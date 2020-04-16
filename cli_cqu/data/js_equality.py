"""与一些 JavaScript 等效的代码"""
from hashlib import md5 as rawmd5

__all__ = ("chkpwd")


def md5(string: str) -> str:
    return rawmd5(string.encode()).hexdigest().upper()


def chkpwd(username: str, password: str) -> str:
    "赋值给: efdfdfuuyyuuckjg"
    schoolcode = "10611"
    return md5(username + md5(password)[0:30].upper() + schoolcode)[0:30].upper()
