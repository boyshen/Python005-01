## 使用说明

### 导入数据
1. 通过 mysql 目录下的sql备份进行导入。导入命令如下：
```
mysql -uroot -p -h127.0.0.1 testdb < comment.sql
mysql -uroot -p -h127.0.0.1 testdb < movie.sql
```

2. 如果不通过以上方式导入数据，可以运行 douban/crawling.py 文件进行爬取豆瓣电影。

### 运行 Django 进行访问
1.访问指定电影的评论
```
http://127.0.0.1:8888/douban/mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce

mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce 为电影的 id. 可在 movie 表中查询到
```
2.访问指定电影3星级以上的评论
```
http://127.0.0.1:8888/douban/mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce/star=3

mid=7e2c3043-59d8-49f4-9aee-6de90ce232ce 为电影的 id
star=3。表示显示 3 星级以上的评论。 
```

(PS：如果是运行 douban/crawling.py 获取的数据，需要查看在 movie 表中查询 mid 值)


