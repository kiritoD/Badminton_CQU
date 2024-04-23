import email
from dataclasses import field
from typing import Dict, List


def display_data(data: Dict):
    area_data = data["data"]
    time_axis_list = area_data["timeAxisList"]
    field_list = area_data["allFieldAndPriceList"]
    field_data_list = []
    for index_x, field_data in enumerate(field_list):
        for index_y, field_item in enumerate(field_data["priceList"]):
            # field_item["filed_id"] = filed_id
            field_item["is_available"] = True if field_item["price"] else False
            field_item["x"] = index_x
            field_item["y"] = index_y
            field_item["field_name"] = field_data["fieldName"]
            field_data_list.append(field_item)
    return field_data_list


def order_data(date: str, order_ids: List[int], data: Dict):
    """
    This function is used to formnat the data for booking.
    Parameters
    ----------
    date : str
        the date of the booking, for example "2024-04-23"
    order_ids : List[int]
        the order ids of the booking, for example [1]
    data : List[int]
        the coressponding data of the booking, for example {"1": {"beginTime": "10:00", "endTime": "12:00", "fieldId": 1 ...}}

    Returns
    -------
    Dict
        _description_
    """
    book_data = {"orderDate": date, "orderDetailList": [], "voucherNos": []}
    for order_id in order_ids:
        data_temp = data[order_id]
        book_data_temp = {
            "beginDate": date,
            "endDate": date,
            "beginTime": data_temp["beginTime"],
            "endTime": data_temp["endTime"],
            "fieldId": data_temp["fieldId"],
            "priceOrig": 12,
            "pricePay": 12,
        }
        book_data["orderDetailList"].append(book_data_temp)
    return book_data
