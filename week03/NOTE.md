## 1. 字符集配置

1. 在 mysql 的配置文件 (/etc/my.conf) 中添加设置。

       ```
       [client]
       default_character_set = utf8mb4
       
       [mysql]
       default_character_set = utf8mb4
       
       # 设置mysql字符集
       character_set_server = utf8mb4
       # 服务器为每个链接客户端执行的字符串
       init_connect = 'SET NAMES utf8mb4'
       # 控制客户端连接握手时候不使用默认的校对规则。使用 collation_server 规定的校对规则。
       character_set_client_handshake = FALSE
       # 设置排序规则。unicode 表示区分大小写，ci 表示大小写不敏感。cs 表示大小写敏感
       collation_server = utf8mb4_unicode_ci
       ```
  
2.  重新启动 mysql
  
       ```
       systemctl restart mysqld.service
       ```
    
3.  查看mysql字符集修改
  
       ```
        show variables like '%character%';
       ```

## 2. 增加远程用户的 SQL 语句

1. 方法一：创建数据库，并进行授权
  
       ```
       create database testdb;
       GRANT ALL PRIVILEGES ON testdb.* TO 'test'@'%' IDENTIFIED BY 'password';
       ```
  
2. 方法二：创建用户，并进行授权
  
       ```
       GRANT ALL PRIVILEGES ON *.* TO 'test'@'%' IDENTIFIED BY 'password' WITH GRANT OPTION;
       ```
  
3. 查看用户权限
  
       ```
       SHOW GRANTS FOR 'test'@'%';
       ```

## 3. SQL 语句标注执行顺序

```
SQL 语句																												执行顺序
SELECT DISTINCT player_id, player_name, count(*) as num 				5
FROM player JOIN team ON player.team_id = team.team_id 					1
WHERE height > 1.80 																						2
GROUP BY player.team_id 																				3
HAVING num > 2 																									4
ORDER BY num DESC 																							6
LIMIT 2																													7
```

## 4. ORM、插入、查询语句

1. ORM

   ```
   class UserTable(Base):
       """
       # 用户 id、用户名、年龄、生日、性别、学历、字段创建时间、字段更新时间
       """
       __tablename__ = 'user'
       uid = Column(BigInteger(), primary_key=True)
       name = Column(String(50), nullable=False)
       age = Column(Integer())
       birthday = Column(Date())
       gender = Column(CHAR(10))
       education = Column(String(50))
       create_time = Column(TIMESTAMP(3), default=get_time())
       update_time = Column(TIMESTAMP(3), onupdate=get_time(), default=get_time()
   ```

2. 插入 & 查询

   ```
   # 插入
   user_info = UserTable(name=name, age=age, birthday=birthday, gender=gender, education=education)
   session.add(user_info)
   
   # 查询所有用户信息
   res = (result for result in session.query(UserTable))
   
   # 指定出生日期做条件查询
   res = (result for result in session.query(UserTable).filter(UserTable.birthday > birthday))
   
   # 根据性别统计用户数量
   res = (result for result in session.query(UserTable.gender, func.count(UserTable.gender)).group_by(UserTable.gender))
   
   # 根据学历统计用户
   query = session.query(UserTable.education, func.count(UserTable.education)).group_by(UserTable.education)
   query = query.order_by(desc(func.count(UserTable.education)))
   ```

## 5. 基于 id 列 INNER JOIN、LEFT JOIN、 RIGHT JOIN 的结果

1. 表 test1 和 test2 的存放数据：

   ```
   mysql> select * from test1;
   +-----+--------+
   | uid | name   |
   +-----+--------+
   |   1 | 张三   |
   |   2 | 李四   |
   |   3 | 王五   |
   |   4 | 赵六   |
   +-----+--------+
   4 rows in set (0.01 sec)
   
   mysql> select * from test2;
   +-----+------+
   | uid | name |
   +-----+------+
   |   2 | zhan |
   |   3 | li   |
   |   4 | wu   |
   |   5 | xu   |
   +-----+------+
   4 rows in set (0.00 sec)
   ```

2. INNER JOIN 结果

   返回 左表和右表中匹配的行。

   ```
   mysql> SELECT test1.uid, test1.name, test2.uid, test2.name  FROM test1 INNER JOIN test2 ON test1.uid = test2.uid;
   +-----+--------+-----+------+
   | uid | name   | uid | name |
   +-----+--------+-----+------+
   |   2 | 李四   |   2 | zhan |
   |   3 | 王五   |   3 | li   |
   |   4 | 赵六   |   4 | wu   |
   +-----+--------+-----+------+
   3 rows in set (0.00 sec)
   ```

3. LEFT  JOIN 结果

   返回左表中的所有行，其中与右表不匹配的使用 NULL 填充

   ```
   mysql> SELECT test1.uid, test1.name, test2.uid, test2.name  FROM test1 LEFT JOIN test2 ON test1.uid = test2.uid;
   +-----+--------+------+------+
   | uid | name   | uid  | name |
   +-----+--------+------+------+
   |   1 | 张三   | NULL | NULL |
   |   2 | 李四   |    2 | zhan |
   |   3 | 王五   |    3 | li   |
   |   4 | 赵六   |    4 | wu   |
   +-----+--------+------+------+
   4 rows in set (0.00 sec)
   ```

4. RIGHT JOIN 结果.

   返回右表中的所有行，其中与左表不匹配的使用 NULL 填充

   ```
   mysql> SELECT test1.uid, test1.name, test2.uid, test2.name  FROM test1 RIGHT JOIN test2 ON test1.uid = test2.uid;
   +------+--------+-----+------+
   | uid  | name   | uid | name |
   +------+--------+-----+------+
   |    2 | 李四   |   2 | zhan |
   |    3 | 王五   |   3 | li   |
   |    4 | 赵六   |   4 | wu   |
   | NULL | NULL   |   5 | xu   |
   +------+--------+-----+------+
   4 rows in set (0.00 sec)
   ```

   ## 6. sql 语句为上题中的 id 和 name 增加索引

   根据 EXPLAIN 返回的信息。两个表中一个使用索引，一个没有索引。增加索引并没有提升效率。

   ```
   mysql> EXPLAIN SELECT * FROM user_has_index WHERE name='Vivienne_w';
   +----+-------------+----------------+------------+------+---------------+------+---------+-------+------+----------+-------------+
   | id | select_type | table          | partitions | type | possible_keys | key  | key_len | ref   | rows | filtered | Extra       |
   +----+-------------+----------------+------------+------+---------------+------+---------+-------+------+----------+-------------+
   |  1 | SIMPLE      | user_has_index | NULL       | ref  | name          | name | 202     | const |  207 |   100.00 | Using index |
   +----+-------------+----------------+------------+------+---------------+------+---------+-------+------+----------+-------------+
   1 row in set, 1 warning (0.00 sec)
   
   mysql> EXPLAIN SELECT * FROM user_no_index WHERE name='Vivienne_w';
   +----+-------------+---------------+------------+------+---------------+------+---------+------+-------+----------+-------------+
   | id | select_type | table         | partitions | type | possible_keys | key  | key_len | ref  | rows  | filtered | Extra       |
   +----+-------------+---------------+------------+------+---------------+------+---------+------+-------+----------+-------------+
   |  1 | SIMPLE      | user_no_index | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 39499 |    10.00 | Using where |
   +----+-------------+---------------+------------+------+---------------+------+---------+------+-------+----------+-------------+
   1 row in set, 1 warning (0.00 sec)
   ```

数据库中使用 B+ 树来提升检索效率。其中有主键索引和普通索引两种，user_has_index 中name建立索引，普通索引保存主键索引，即在查询到普通索引时候，再从普通索引中查询到主键索引，再从主键索引中查询到信息。这个过程叫做 回表。所以对于 id 和 name 两个字段建立索引与不建立索引并没有明显的提升效率。除非在某些场景下，比如根据身份证、年龄查询用户，可以给name建立索引，利用索引重置提升效率。

