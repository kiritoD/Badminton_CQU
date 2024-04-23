import json
import logging
import logging.config
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from typing import Callable, Dict, List, Optional, Union

import jsonlines
import numpy as np
from colorama import Fore
from prettytable import PrettyTable
from tqdm import tqdm

from .config import LOGGER_CONFIG, load_yaml

Default_DATA_PATH = os.path.join(os.path.dirname(__file__), "default_data.jsonl")

logging.config.dictConfig(config=LOGGER_CONFIG)

log_levels = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

Colors = {
    "False": Fore.RED,
    "True": Fore.GREEN,
}


def _get_library_name() -> str:
    return __name__.split(".")[0]


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger with the specified name.

    This function is not supposed to be directly accessed unless you are writing a custom transformers module.
    """

    if name is None:
        name = _get_library_name()

    return logging.getLogger(name)


def send_email(
    email_smtp_server: str,
    email_smtp_username: str,
    email_smtp_password: str,
    email_smtp_port: int,
    recipient: str,
    subject: str,
    body: str,
):
    """
    Send an email using the specified SMTP server.
    """
    FROM = email_smtp_username
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    me = f"Badminton <{email_smtp_username}>"
    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = Header(subject, "utf-8")

    message["From"] = me
    message["To"] = f"<{recipient}>"
    try:
        server = smtplib.SMTP(email_smtp_server, email_smtp_port)
        server.ehlo()
        server.starttls()
        server.login(email_smtp_username, email_smtp_password)
        server.sendmail(FROM, TO, message.as_string())
        server.close()
        return True
    except:
        return False


def jsonl_read(path: str):
    data = []
    with open(path, encoding="utf-8") as reader:
        for line in tqdm(reader):
            obj = json.loads(line.strip())
            data.append(obj)
    return data


def jsonl_write(path: str, data: List[Dict]):
    with jsonlines.open(path, mode="w") as writer:
        writer.write_all(data)


def list_badminton_info(date: str, data: Union[Dict, None] = None):
    """list all badminton information"""
    if not data:
        global Default_DATA_PATH
        data = jsonl_read(Default_DATA_PATH)
    data_sorted = sorted(data, key=lambda x: int(x["x"] * 100 + x["y"]))
    data_sorted_dict = {f"{_}": item for _, item in enumerate(data_sorted)}
    fields_x = sorted(set([_["field_name"] for _ in data_sorted]))
    fields_y = sorted(
        set([_["beginTime"][:-3] + "~" + _["endTime"][:-3] for _ in data_sorted])
    )
    display_key = np.array(list(data_sorted_dict.keys()))
    display_key = np.array(
        list(
            map(
                lambda x: Colors[str(data_sorted_dict[x]["is_available"])]
                + x
                + Fore.BLUE,
                display_key,
            )
        )
    )
    display_key_new = display_key.reshape(len(fields_x), len(fields_y)).T
    badminton_table = PrettyTable()
    badminton_table.title = f"{date} CQU 羽毛球馆信息({Fore.GREEN}绿色表示空余，{Fore.RED}红色表示已被预约{Fore.BLUE})"
    badminton_table.field_names = [""] + list(fields_x)
    for index, field_y in enumerate(fields_y):
        badminton_table.add_row([field_y] + list(display_key_new[index]))
    # setting
    # badminton_table.align["model_name"] = "l"
    # badminton_table.align["description"] = "l"
    return badminton_table, data_sorted_dict
