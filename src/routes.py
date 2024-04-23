import json
import time
from datetime import datetime
from typing import Any, Dict, Union

import requests

from .utils import get_logger

logger = get_logger("Route")


class Router:
    def __init__(self, route_setting: Dict, headers_data: Dict):
        """general settings for the route

        Parameters
        ----------
        route_setting : Dict
            about the route information
        headers_data : Dict
            about the headers information
        """
        self.route_setting = route_setting
        self.headers_ = headers_data
        self.token = headers_data["Lg-Authorization"]

    @property
    def headers(self):
        if self.token is not None:
            self.headers_["Lg-Authorization"] = self.token
        return self.headers_

    @classmethod
    def login(cls, username: str, password: str):
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJsZyIsInRlbmFudENvZGUiOiJjcXUiLCJleHAiOjE3MTQzNzkwNjAsInVzZXJJZCI6IjE3Njg0Nzg3NTg1MTc0NzMyODIiLCJpYXQiOjE3MTM3NzQyNjAsInVzZXJuYW1lIjoi6JGj5L-K5LyfIn0.AlV-LHkn9FTOB27VhNZB7p_m0R6NAjhXVwCjTw6Slak"
        return token

    def display(self, date: Union[None, str] = None):
        """display the badminton information for a specical day

        Parameters
        ----------
        date : Union[None, str], optional
            the query date, such as "2024-04-23" ,by default None
        """

        def time_diff(t1, t2):
            try:
                t1_ = datetime.strptime(t1, "%Y-%m-%d")
                t2_ = datetime.strptime(t2, "%Y-%m-%d")
                day_diff = abs((t2_ - t1_).days)
                return day_diff
            except:
                return -1

        current_date = time.strftime("%Y-%m-%d", time.localtime())
        if date is None:
            date = time.strftime("%Y-%m-%d", time.localtime())
        time_diff_threshold = self.route_setting["display"]["settings"][
            "time_diff_threshold"
        ]
        time_diff_value = time_diff(date, current_date)
        if time_diff_value > time_diff_threshold:
            logger.warning(
                f"the maximum time difference is `{time_diff_threshold}` days, please check the date `{date}`!"
            )
            return False
        elif time_diff_value == -1:
            logger.error(
                f"Invalid date format `{date}`, please follow the format: yyyy-mm-dd!"
            )
            return False
        else:
            body_request = self.route_setting["display"]["body"]
            body_request["queryDate"] = date
            display_request = requests.get(
                self.route_setting["display"]["url"],
                params=body_request,
                headers=self.headers,
            )
            if display_request.status_code == 200:
                return json.loads(display_request.text)
            else:
                logger.error(
                    f"request failed, error code:{display_request.status_code}"
                )
                return False

    def book(self, data: Dict[str, Any], La_A: Union[str, None] = None):
        body_request = self.route_setting["book"]["body"]
        headers = self.headers
        if La_A:
            headers["Lg-Authorization"] = La_A
        others = {
            "Content-Type": "application/json",
            "Accept": "*/*",
        }
        headers.update(others)
        body_request.update(data)
        book_request = requests.post(
            self.route_setting["book"]["url"],
            data=json.dumps(body_request),
            headers=headers,
        )
        if book_request.status_code == 200:
            return_data = json.loads(book_request.text)
            return dict(success=True, data=return_data["data"])
        else:
            return dict(success=False, data={})

    def cancel(self, order_id: str): ...
