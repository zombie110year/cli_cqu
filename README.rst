CLI CQU
#######

重庆大学（CQU）的命令行客户端

提供以下功能：

- 下载课表
    -   保存为 JSON，便于后续处理（字段定义参考 `cli_cqu.model` 模块）
    -   保存为 ICalendar 日历日程，可导入 Outlook 等日历应用
- 查询成绩
    -   通过老教务网的接口获取成绩单

使用
====

CLI CQU 提供了命令行界面。

1. 交互式命令行界面

你可以直接运行命令

.. code:: sh

    cli-cqu

进入交互式命令行。在命令提示符

.. code:: text

    username>
    password>

后输入校园帐号（学号）和密码（校园卡查询密码）。
即可完成登录，然后执行命令：

.. code:: text

    cli cqu> help

查看支持的指令以及用法。

2. 命令行参数一次性执行

你可以在命令行中使用 `-u` 和 `-p` 参数直接登录，并且直接传入要执行的指令。如

.. code:: sh

    cli-cqu -u 20770000 -p zombie110year help

将直接登录 `20770000` 帐号并执行 `help`

3. 查询成绩

为了避免由于某学期未评教导致无法在 jxgl 网上查询成绩而使用了老教务网的接口。
老教务网只能通过学校内网访问，在外网需要连接 VPN。

由于老教务网的登录密码和 jxgl 不一样，因此只能通过命令行调用来使用此功能。
默认的密码是身份证后 6 位：

.. code:: sh

    cli-cqu -u 20770000 -p 123456 assignments-json

之后将会从老教务网获取成绩单，并解析为 JSON 保存。

安装
====

你可以使用 pip 安装，由于使用了 f-string，需要 python 3.6 以上：

.. code:: sh

    pip install cli-cqu

或者使用 pipx 安装（TODO）：

.. code:: sh

    pipx install cli-cqu

贡献
====

此项目基于 MIT 协议发行，你可以在遵守协议的情况下做任何事。

下面是本项目各模块的介绍

- `cli_cqu` App 对象和命令行接口
    - `cli_cqu.data` 模块是需要用到的数据，例如常量、路由、解析规则（函数）等。
        - `cli_cqu.data.ua` User-Agent。
        - `cli_cqu.data.js_equality` 与 jxgl 网页前端的 js 等效的一些函数。
        - `cli_cqu.data.route` 路由，根据 jxgl 的功能模块分类
    - `cli_cqu.exception` 定义的一些异常
        - `cli_cqu.exception.signal` 充当信号作用的异常
    - `cli_cqu.model` 数据模型
