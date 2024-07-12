## Badminton For CQU

This is a project for CQU Badminton schedule. [Anonymous development]

## Install

```python
# python 3.10+ required
pip install -r requirements.txt
```
## Usage

```
python main.py
```
## config/settings.yaml

```yaml
users:
  user_name: xxx
route:
  user:
    url: http://huxispce.cqu.edu.cn/api/weixin/auth/login
    type: post
  book:
    url: http://huxispce.cqu.edu.cn/api/field/wechat/fieldReserve/createFieldReserveOrder
    type: post
    body:
      cardId: null
      fieldAreaId: 1704745389682458625
      itemId: "1"
      orderDate: "2024-04-23"
      orderDetailList:
        - beginDate: 2024-04-23
          beginTime: "21:00:00"
          endDate: "2024-04-23"
          endTime: "22:00:00"
          fieldId: "1706485299959431169"
          priceOrig: 12
          pricePay: 12
      orderType: R
      priceOrig: 12
      pricePay: 12
      saleMode: F
      venueId: 1704736567056269314
      voucherNos:
        - null
    return_field: success, data.orderId # return key
  display:
    url: http://huxispce.cqu.edu.cn/api/field/wechat/fieldReserve/getFieldReserveDisplayData
    type: get
    settings:
      time_diff_threshold: 2 # time difference between local time and target time in days

    body:
      venueId: 1704736567056269314
      areaId: 1704745389682458625
      queryDate: 2024-04-23
      isVirtual: F
  cancel:
    url: http://huxispce.cqu.edu.cn/api/weixin/myOrder/cancelOrder
    type: get
    body:
      orderId: null
email:
  email_smtp_server: smtp.qq.com
  email_smtp_port: 587
  email_smtp_username: xxx@qq.com
  email_smtp_password: xxx
```

## Features

#### 2024-04-23
- [x] regular venue booking
- [x] terminal gui
- [x] email notification
#### 2024-04-21
- [x] start
