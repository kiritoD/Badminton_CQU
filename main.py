import os
import re
from datetime import datetime
from functools import partial
from typing import Any, Callable, Counter, Literal, Union

from colorama import Fore
from fake_useragent import UserAgent

from src.mp_tool import MP_Tool, schedule_task
from src.parese import display_data, order_data
from src.routes import Router
from src.terminal_util import *
from src.utils import get_logger, list_badminton_info, load_yaml, send_email

logger = get_logger("Badminton")
Config_Settings = load_yaml(
    f"{os.path.abspath(os.path.dirname(__file__))}/config/settings.yaml"
)

send_email = partial(
    send_email,
    Config_Settings["email"]["email_smtp_server"],
    Config_Settings["email"]["email_smtp_username"],
    Config_Settings["email"]["email_smtp_password"],
    Config_Settings["email"]["email_smtp_port"],
)


UA = UserAgent()
token = Router.login(None, None)
Header = {
    "Lg-Authorization": token,
    "User-Agent": UA.random,
}

Router_Badminton = Router(Config_Settings["route"], Header)


def text_format(text, color="WHITE"):
    print(getattr(Fore, color) + f"{text:<50} ")


def main(MP):

    prompt = """请先在./config/settings.yaml中将你的`Lg-Authorization`码放进去, 数量要>=你要抢的场地数量，否则失败...
获取`Lg-Authorization`码的方式：在 https://sso.cqu.edu.cn/login网站上登录你的账号，然后F12，随便找一个请求，
在请求头里面找到`Lg-Authorization`字段，将该字段copy，然后填到settings.yaml中的users下面即可，参照示例：
users:
    xxx: La-Au...
    yyy: La-Au...
    mmm: La-Au...
Attention:
    1. 如果你在其他地方登陆过你的账号，那么你可能需要重新填一下你的`Lg-Authorization`码
    2. 为了安全，不调用系统命令创建定时任务，因此程序只要结束，所有子进程全部杀死
    3. 简单测试发现无法直接获取La, 可以通过selenium来搞，但是懒了
    4. 在Linux终端用tmux来创建守护进程，这样只要电脑不关就类似定时任务了
    """
    text_format(prompt, "RED")
    # text_format(prompt)
    while True:
        confirme = input(Fore.WHITE + "我弄好并且明白了? (y): ")
        if confirme == "n":
            exit()
        elif confirme == "y":
            users = Config_Settings["users"].values()
            user_length = len(users)
            if user_length == 0:
                text_format("你没有一个用户，请参照提示重新添加!!!")
            else:
                break
    os.system("clear")
    users = list(Config_Settings["users"].values())
    user_length = len(users)
    text_format(
        f"你提供了{Fore.RED}{user_length}{Fore.WHITE}个账号，最多抢{Fore.RED}{user_length}{Fore.WHITE}个场地！"
    )

    # date part
    counter = 0
    while True:
        date = input(Fore.WHITE + "请输入你想预定的日子(格式：xxxx-xx-xx/2024-04-24): ")
        counter += 1
        format_time = "%Y-%m-%d"
        try:
            t = datetime.strptime(date, format_time)
            t_current = datetime.strptime(
                datetime.now().strftime(format_time), format_time
            )
            if t < t_current:
                text_format(f"你丫的想回到过去{date}打球吗?", "RED")
                counter += 1
            else:
                break
        except:
            text_format(f"检查格式", "RED")
            counter += 1
    clear_lines_from_b_to_u(counter - 1)
    data_areas: Any | Literal[False] = Router_Badminton.display(date)
    if not data_areas:
        data_areas_post = None
    else:
        data_areas_post = display_data(data_areas)
    data_table, data_sorted_dict = list_badminton_info(date, data_areas_post)
    text_format(str(data_table), "BLUE")
    counter = -1
    ids_ = []

    # area numbers
    while True:
        try:
            text_format(
                f"请输入你想抢的场地号码(0-{len(data_sorted_dict)}, 如果是多个场地请用,隔开).",
                "GREEN",
            )
            counter += 1
            ids = input("请输入: ")
            counter += 1
            ids_ = ids.split(",")
            ids_ = list(map(lambda x: int(x.strip()), ids_))
            if len(ids_) > user_length:
                text_format("人数超了!", "RED")
                counter += 1
            else:
                break
        except:
            text_format(f"检查格式", "RED")
            counter += 1
    clear_lines_from_b_to_u(counter)
    text_format(f"你要预定的场地有: {ids_}", "GREEN")

    # email part
    email_reg = (
        r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$"
    )
    counter = -1
    email_url = None
    while True:
        email_url = input(Fore.WHITE + "请输入接受通知的中国大陆邮箱: ")
        counter += 1
        if re.match(email_reg, email_url):
            break
        else:
            text_format("请检查邮箱！", "RED")
            counter += 1
    clear_lines_from_b_to_u(counter)
    text_format(f"你的邮箱地址是: {email_url}", "GREEN")

    # time part
    counter = -1
    time_ = None
    while True:
        time_ = input("请输出任务开始时间(xx:xx/18:00, 如果是-1，那么就立马抢！): ")
        counter += 1
        if time_ == "-1":
            time_ = None
            break
        else:
            # lazy to reg
            ...
            break
    clear_lines_from_b_to_u(counter)
    time_str = "Now" if not time_ else time_
    text_format(f"任务执行时间为:{time_str}", "GREEN")

    # book part
    text_format(f"开始启动多进程处理任务...", "BLUE")
    results = []
    for id_, La_A in zip(ids_, users[: len(ids_)]):
        text_format(f"正在为场地{id_}创建任务", "BLUE")
        book_data = order_data(date, [str(id_)], data_sorted_dict)
        result = schedule_task(
            MP, Router_Badminton.book, email_url, time_, send_email, book_data, La_A
        )
        text_format(f"场地{id_}抢占任务创建完成.", "BLUE")
        results.append(result)
    text_format(f"所有任务正在排队或者执行...(ctrl+c 终止所有程序)")
    for result_ in results:
        result_.wait()

    # end
    text_format(
        f"所有信息都已经转发到你的邮箱{email_url}, 请记得查收！\n 祝你健康快乐！！！",
        "GREEN",
    )


if __name__ == "__main__":
    MP = MP_Tool()
    main(MP)
