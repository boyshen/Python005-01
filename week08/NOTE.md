## Homework 
查看 server 目录

## 使用说明
1. 参考django配置mysql相关信息并执行数据库列表创建
2. 创建用户。
```
# python manage.py createsuperuser --email admin@example.com --username admin
```

3. 运行服务
```
# python manage.py runserver
```

4. 操作

4.1 创建订单。提示需要登录认证
```
# http POST http://127.0.0.1:8000/api/v1/order/create commodity='food'

{
    "detail": "Authentication credentials were not provided."
}
```

4.2 登录创建订单。返回订单信息
```
# http -a admin:123qwe POST http://127.0.0.1:8000/api/v1/order/create commodity='food'

{
    "cancel": "http://127.0.0.1:8000/api/v1/order/1/cancel",
    "commodity": "food",
    "created": "2021-01-13T07:07:04.877819Z",
    "id": 1,
    "owner": "admin",
    "remarks": "null",
    "status": "Normal",
    "url": "http://127.0.0.1:8000/api/v1/order/1"
}
```

4.3 查看指定订单信息
```
# http -a admin:123qwe http://127.0.0.1:8000/api/v1/order/1

{
    "cancel": "http://127.0.0.1:8000/api/v1/order/1/cancel",
    "commodity": "food",
    "created": "2021-01-13T07:07:04.877819Z",
    "id": 1,
    "owner": "admin",
    "remarks": "null",
    "status": "Normal",
    "url": "http://127.0.0.1:8000/api/v1/order/1"
}
```

4.4 取消订单
```
# 取消订单。返回 ok
# http -a admin:123qwe http://127.0.0.1:8000/api/v1/order/1/cancel

# 查看订单信息
# http -a admin:123qwe http://127.0.0.1:8000/api/v1/order/1

{
    "cancel": "http://127.0.0.1:8000/api/v1/order/1/cancel",
    "commodity": "food",
    "created": "2021-01-13T07:07:04.877819Z",
    "id": 1,
    "owner": "admin",
    "remarks": "null",
    "status": "Cancelled",  # 订单状态改变。由 'Normal' 变成 'Cancelled'
    "url": "http://127.0.0.1:8000/api/v1/order/1"
}
```

4.5 订单列表
```
# http -a admin:123qwe http://127.0.0.1:8000/api/v1/order

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "cancel": "http://127.0.0.1:8000/api/v1/order/1/cancel",
            "commodity": "food",
            "created": "2021-01-13T07:07:04.877819Z",
            "id": 1,
            "owner": "admin",
            "remarks": "null",
            "status": "Cancelled",
            "url": "http://127.0.0.1:8000/api/v1/order/1"
        },
        {
            "cancel": "http://127.0.0.1:8000/api/v1/order/2/cancel",
            "commodity": "software",
            "created": "2021-01-13T07:13:50.292582Z",
            "id": 2,
            "owner": "admin",
            "remarks": "null",
            "status": "Normal",
            "url": "http://127.0.0.1:8000/api/v1/order/2"
        }
    ]
}
```


