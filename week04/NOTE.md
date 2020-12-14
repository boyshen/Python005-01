5. Django Web 开发入门
5.1 开发环境配置
  ● 简介
      ○ Django 是一个开放源代码的 Web 应用框架。
      ○ Django 最初被设计用于具有快速开发需求的新闻类站点，目的是要实现简单快捷的网站开发
  ● Django 的特点
      ○ 1. 采用 MTV 的框架。
          ■ 模型 (Model)、模板 (Template)、视图 (Views)

      ○ 2. 强调快速开发和代码复用 DRY (Do Not Repeat Yourself)
      ○ 3. 组件丰富
          ■ ORM (对象关系映射) 映射类来构建数据模型
          ■ URL 支持正则表达式
          ■ 模板可继承
          ■ 内置用户认证，提供用户认证和权限功能
          ■ admin 管理系统
          ■ 内置表单模型、Cache 缓存系统、国际化系统等
  ● Django 安装
      ○ 参考：https://docs.djangoproject.com/zh-hans/3.0/intro/install/.
      ○ 安装：
          ■ pip install --upgrade django==2.2.13
      ○ 验证：
          ■ import django
          ■ django.__version__
          

5.2 创建项目和应用程序
  ● 创建项目
      ○ django-admin startproject [MyDjango  Django 项目名称] 
      ○ 项目相关配置文件
          ■ MyDjango//MyDjango/settings.py  项目配置文件
          ■ MyDjango//manage.py     命令行工具
          ■ MyDjango//MyDjango/urls.py    项目与应用程序连接配置
  ● 创建应用程序
      ○ python manage.py startapp [index 应用程序名称]
      ○ 应用程序相关文件
          ■ index/migrations  数据库迁移文件
          ■ index/models.py 模型
          ■ index/apps.py   当前应用程序配置文件
          ■ index/admin.py    管理后台
          ■ index/tests.py    自动化测试
          ■ index/views.py    视图
  ● 启动 Django 服务
      ○ python manage.py runserver
      ○ python manage.py runserver 0.0.0.0:8888

5.3 settings.py  配置文件
  ● 配置文件包括的内容
      ○ 项目路径
      ○ 密钥
      ○ 域名访问权限
      ○ APP 列表
      ○ 静态文件，包括 CSS、JavaScript 、图片等
      ○ 模板文件
      ○ 数据库配置
          ■ 参考：https://docs.djangoproject.com/zh-hans/3.0/ref/databases/#mysql-notes
      ○ 缓存
      ○ 中间件

5.4 Django 如何处理请求
  ● 当一个用户请求 Django 站点的一个页面
      ○ 1. 如果传入的 HttpRequest 对象拥有 urlconf 属性（通过中间件设置），它的值将被用来代替 ROOT_URLCONF 设置。
          ■ setting 配置文件中
      ○ 2. Django 加载 URLconf 模块并寻找可用的 urlpatterns，Django 依次匹配每个 URL 模式，在与请求的 URL 匹配的第一个模式停下来
      ○ 3. 匹配成功。
          ■ 3.1. Django 会在 setting 中找到对应的 APP 。同时获得 HttpRequest 实例和相关参数。
          ■ 3.2. 通过注册的 APP 找到在 APP 目录下的 url 文件(url.py 文件需要手动创建)。同时找到url文件中对应的 urlpatterns，找到对应的响应函数。
          ■ 3.3. 执行响应函数。


      ○ 4. 如果没有 URL 被匹配，或者匹配过程中出现异常，Django 会调用一个适当的错误处理视图
5.5 让 URL 支持变量
  ●  让 URL 支持变量的三种方式：类型模式、正则表达式、自定义匹配规则
  ● 1. 类型模式支持：str、int、slug、uuid、path
      ○ 使用方法。在APP应用程序目录下的 url.py 文件中添加。例如：
      ○ 同时对应的在 views 文件中添加响应函数
      ○ 请求方式在 URL 连接后添加数字或字符
  ● 2. 正则表达式模式。
      ○ 注意需要使用 re_path 模块。同样在应用程序 APP 下的 url 文件中 urlpatterns 中添加
      ○ 对应的在应用程序下 views 中添加响应函数。

  ● 3. 自定义模式
      ○ 3.1 定义转换函数。可在当前目录下新建 converts.py 文件。定义转换函数的类
          ■ 注意正则表达格式和函数名称必须一样。
      ○ 3.2 注册转换函数
          ■ 在应用程序的 url.py 配置文件中，导入 django 中的 reister_convert 模块，注册转换函数。
      ○ 3.3 配置path。其中 myint 为注册函数中替换 url 的名称。

5.6 view 视图
  ● 快捷函数
      ○ render（绑定）
          ■ 将给定的模板与上下文字典组合在一起，并以渲染的文本返回一个 HttpResponse 对象
      ○ redirect (重定向)
      ○ get_object_or_404
          ■ 在给定的模型管理器(model manager) 上调用 get(), 但它会引发 http404 而不是模型的 DoesNotExists 异常。

5.7.1 创建模型
  ● 1. 安装 mysql-client
      ○ 1.1 参考：https://docs.djangoproject.com/zh-hans/3.0/ref/databases/#mysql-notes
      ○ 1.2 配置环境变量
          ■ export PATH=$PATH:/usr/local/mysql/bin

      ○ 1.3 安装第三方依赖包
          ■ pip install mysqlclient
          ■ pip install pymysql 
  ● 2. 在 setting 中配置使用 mysql 。

  ● 3. 创建模型，在应用程序的 model.py 文件中进行添加。
      ○ 每个模型(即数据库)都是一个 python 的类， 这些类继承 django.db.models.Model。
          ■ 其中 id 会自动创建并设置为主键
          ■ 模型类的每个属性都相当于一个数据库的字段。


  ● 4. 执行迁移
      ○ python manage.py makemigrations index 
          ■ # 根据模型信息进行创建新的迁移，当模型信息改变时候，会生成新的迁移。[index] 为应用程序
      ○ python manage.py migrate    
          ■ # 执行迁移
      ○ sqlmigrate，显示用于迁移的SQL语句。
      ○ showmigrations，其中列出了项目的迁移及其状态。其中 [X] 表示已经迁移，[] 表示没有迁移。

5.7.2 模型操作
  ● 使用 Diango 提供的 manage.py shell 进行测试模型。
      ○ python manage.py shell
  ● 增
      ○ from index.models import *
      ○ Name 为模型对象
      ○ 方法一：
          ■ Name.objects.create(name='红楼梦', author='曹雪芹', stars='9.6')
      ○ 方法二：
          ■ n = Name()
          ■ n.name='红楼梦'
          ■ n.author='曹雪芹'
          ■ n.stars=9.6
          ■ n.save()  # save 写入数据
  ● 删
      ○ 删除一条
          ■ Name.objects.filter(name='红楼梦').delete()
      ○ 删除所有
          ■ Name.objects.all().delete()
  ● 改
      ○ Name.objects.filter(name='红楼梦').update(name='石头记')
  ● 逻辑查询
      ○ __gte : 大于等于
      ○ __lt: 小于
      ○ __gt: 大于
      ○ __lte: 小于等于
      ○ 示例一：Django 中使用 __ 来区分。__ 的前面为查询的字段，后面为逻辑运算。该方法需要先得到 queryset 。查看 values 用法
          ■ queryset = T1.objects.values('sentiment')
          ■ condtions = {'sentiment__gte': 0.5}
          ■ plus = queryset.filter(**condtions).count()
      ○ 示例二：
          ■ queryset = T1.objects.values('sentiment')
          ■ condtions = {'sentiment__lt': 0.5}
          ■ minus = queryset.filter(**condtions).count()
  ● 条件查询
  ● 聚合函数
          ■ Name.objects.values_list('name').count()
          ■ T1.objects.aggregate(Avg('n_star'))

5.8 模板
  ● 模板变量 {{ variables }}
  ● 从 URL 获取模板变量 {% url 'urlyear' 2020 %}  其中 url 指定从 url中获取，‘urlyear’ 为url中的name。
  ● 读取静态资源内容 {% static "css/header.css" %}
  ● for 遍历标签 {% for type in type_list %} {% endfor %}
  ● if 判断标签 {% if name.type==type.type %}{% endif %}

5.9 反向创建Models
  ● 反向创建 Models。即根据数据库中已有的表创建映射到 Models.py 文件中
  ● 1. 编辑 setting.py 文件。指定连接的数据库等相关信息。
  ● 2. 执行，输出可以映射 Model 程序，使用 > 将数据流输入到指定文件中。
      ○ python manage.py inspectdb 
      ○ 或：python manage.py inspectdb > models.py

5.10 Bootstrap 框架了解 
  ● 获取 bootstrap 
  ● 通过文档了解 bootstrap 