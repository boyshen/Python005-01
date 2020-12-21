# -*- encoding: utf-8 -*-
"""
@file: string_.py
@time: 2020/12/19 下午5:10
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
import redis


def main():
    client = redis.Redis("192.168.0.197", port=6379, password='P@ssw0rd')

    # 存储
    # client.sadd('set_demo', 'data1')
    # client.sadd('set_demo', 'data2')
    # client.sadd('set_demo', 'data3')
    #
    # # 从随机弹出一个元素
    # data = client.spop('set_demo')
    # print(data)
    #
    # # 获取集合中的所有的元素
    # # 返回：{b'data3', b'data2'}
    # data = client.smembers('set_demo')
    # print(data)
    #
    # client.sadd('set_demo1', 'data1')
    # client.sadd('set_demo1', 'data2')
    # client.sadd('set_demo1', 'data4')
    #
    # # 交集
    # # 返回：{b'data2'}
    # data = client.sinter('set_demo', 'set_demo1')
    # print(data)

    # 并集
    # 返回：{b'data4', b'data2', b'data1', b'data3'}
    data = client.sunion('set_demo', 'set_demo1')
    print(data)

    # 差集。返回第二个集合中缺少的元素
    # 返回：{b'data3'}
    data = client.sdiff('set_demo', 'set_demo1')
    print(data)

    # # 存储.
    # client.zadd('rank', {'a': 1, 'b': 3, 'c': 2, 'd': 5, 'e': 4, 'f': 10})
    #
    # # 读取
    # # 根据评分输出排序。选择读取一定范围内的数据.
    # # min, max 指定读取的数据范围.
    # # withscores 显示评分
    # # 返回：[(b'a', 1.0), (b'c', 2.0), (b'b', 3.0), (b'e', 4.0), (b'd', 5.0)]
    # data = client.zrangebyscore('rank', min=1, max=5, withscores=True)
    # print(data)
    #
    # # 返回当前有序集合中元素的数量
    # data = client.zcard('rank')
    # print(data)
    #
    # # 返回从小到大排序结果。
    # # start, end 为数据索引。建立在排序的基础上
    # # 返回 [(b'c', 2.0), (b'b', 3.0), (b'e', 4.0), (b'd', 5.0), (b'f', 10.0)]
    # data = client.zrange('rank', start=1, end=-1, withscores=True)
    # print(data)
    #
    # # 返回从大到小的排序结果
    # # start, end 为数据索引。建立在排序的基础上
    # # 返回 [(b'f', 10.0), (b'd', 5.0), (b'e', 4.0)]
    # data = client.zrevrange('rank', start=0, end=2, withscores=True)
    # print(data)
    #
    # # 修改某个评分值。amount 为修改的值。value 为对应的key
    # client.zincrby('rank', amount=-2, value='e')

    # # 存数据到哈希。'vip':哈希表名，'user_id':key, 'value': value
    # client.hset('vip', 'user_id1', 'value1')
    #
    # # 判断 key 是否存在
    # result = client.hexists('vip', 'user_id4')
    # print(result)
    #
    # # 添加多个 key 和 value
    # client.hmset('vip', {'user_id3': 'value3', 'user_id4': 'value5'})
    #
    # # 查看所有的 key 值
    # data = client.hkeys('vip')
    # print(data)
    #
    # # 获取某个 key 值
    # data = client.hget('vip', 'user_id3')
    # print(data)
    #
    # # 获取所有的 key 和 value
    # data = client.hgetall('vip')
    # print(data)

    # # 加入列表数据。lpush 从左加入和 rpush 从右加入
    # client.lpush('list_redis', 'value1')
    # client.rpush('list_redis', 'value2')
    #
    # # 查看长度
    # size = client.llen('list_redis')
    # print(size)
    #
    # # 弹出数据, lpop(), rpop()
    # data1 = client.lpop('list_redis')
    # data2 = client.rpop('list_redis')
    # print(data1)
    # print(data2)
    #
    # # 查看一定范围内的列表数据
    # data = client.lrange('list_redis', 0, -1)
    # print(data)

    # client.set('key', 'value1')
    # client.set('key', 'value3')
    # # nx = True 表示不更新当前的 value。 默认更新 value
    # client.set('key', 'value2', nx=True)
    #
    # # 叠加字符串
    # client.append('key', 'value5')
    #
    # # 数字相加。amount 为需要加/减的值
    # client.set('key2', '10')
    # client.incr('key2', amount=2)
    #
    # # 数字相减.
    # client.decr('key2', amount=4)
    #
    # result = client.get('key2')
    # print(result.decode())


if __name__ == '__main__':
    main()
