重庆大学（CQU）的命令行客户端

提供以下功能：

- 下载课表
    -   保存为 JSON，便于后续处理（字段定义参考 ``cli_cqu.model`` 模块）
    -   保存为 ICalendar 日历日程，可导入 Outlook 等日历应用
- 查询成绩
    -   通过老教务网的接口获取成绩单

使用
====

在命令行运行可执行程序 ``cli-cqu`` 即可进入 CLI CQU 的交互式 Shell 中，可以采用类似于命令行的操作方式。
进入 REPL 后，提示符被替换为 ``cli cqu>`` 。

第一次运行时，需要输入用户名与密码，分别需要教学管理（jxgl）和老教务网（oldjw）的两个帐号，两个帐号的密码不一定相同，一般来说，老教务网的密码会是初始密码（身份证后 6 位）。
账户信息会保存到本地（ ``~/.config/cli-cqu/account.toml`` ），之后使用时会直接从文件读取，而无需手动输入。如果有更改，需自行修改文件内容。

1. 退出程序::

    exit

2. 查询帮助::

    help [command_name]

当无参数时，此命令会显示程序整体的帮助信息；当后缀一个命令名时，将显示对应命令的帮助信息。

3. 下载课程表（JSON 格式）::

    courses-json filename

将 **当前学期** 的课程表内容下载为 JSON 文件至 filename 所指定的路径。

4. 下载课程表（Ical 格式）::

    courses-ical filename startdate

将 **当前学期** 的课程表内容下载为 ICalendar 日志格式至 filename 所指定的路径。

5. 下载全部成绩（JSON 格式）::

    assignments-json filename

将 **所有学期的全部科目** 的成绩以 JSON 的格式下载至 filename 指定的路径。

安装
====

你可以使用 pip 安装，由于使用了 f-string，需要 python 3.6 以上::

    pip install cli-cqu

或者使用 pipx ::

    pipx install cli-cqu

贡献
====

此项目基于 MIT 协议发行，你可以在遵守协议的情况下做任何事。

下面是本项目各模块的介绍

- ``cli_cqu`` App 对象和命令行接口
    - ``cli_cqu.login`` 模块是登录功能
    - ``cli_cqu.data`` 模块是需要用到的数据，例如常量、路由、解析规则（函数）等。
        - ``cli_cqu.data.ua`` User-Agent。
        - ``cli_cqu.data.js_equality`` 与 jxgl 网页前端的 js 等效的一些函数。
        - ``cli_cqu.data.route`` 路由，根据 jxgl 的功能模块分类
        - ``cli_cqu.data.schedule`` 日程表
    - ``cli_cqu.model`` 数据模型
    - ``cli_cqu.util`` 其他辅助功能
