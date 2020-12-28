# -*- encoding: utf-8 -*-
"""
@file: attr.py
@time: 2020/12/26 下午12:56
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""


class Age(object):
    def __init__(self):
        self.age = 10

    def __set__(self, instance, value):
        # 对属性值进行指定范围限制
        if value not in [18, 25]:
            raise ValueError("must be in [18, 25]")
        self.age = value

    def __get__(self, instance, owner):
        print(instance.__class__ == owner)
        print("instance: {}, owner:{}".format(instance, owner))
        return self.age


class Human(object):
    age = Age()
    _age = 19

    def __init__(self):
        self.__name = 'zhang'

    #
    # @property
    # def name(self):
    #     return self.__name
    #
    # @name.setter
    # def name(self, value):
    #     self.__name = value
    #
    # @name.deleter
    # def name(self):
    #     del self.__name
    # def __set__(self, instance, value):
    #     # 对属性值进行指定范围限制
    #     if value not in [18, 25]:
    #         raise ValueError("must be in [18, 25]")
    #     self.age = value

    def __getattr__(self, item):
        print("get attr item:{}".format(item))
        return "Error not found"

    def __getattribute__(self, item):
        print("get attribute item:{}".format(item))
        return super().__getattribute__(item)

    # def __getattr__(self, item):
    #     """
    #     重写 getattr 方法。对指定属性进行处理
    #     属性不在 __dict__ 中，调用该方法。
    #     :param item:
    #     :return:
    #     """
    #     print("get attr item:{} ".format(item))
    #     self.item = item
    #     # 属性名等于 'fly' 的进行处理。返回 'OK'， 其他属性返回 None
    #     if self.item == 'fly':
    #         return 'OK'
    # def __getattr__(self, item):
    #     """
    #     重写 getattr 方法。对不存在的属性进行处理。返回一个默认的值.
    #     属性不在 __dict__ 中，调用该方法
    #     :param item:
    #     :return:
    #     """
    #     print("get attr item:{} ".format(item))
    #     return 'OK'
    # def __getattribute__(self, item):
    #     """
    #     对实例获取属性的方法进行重写。将不存在的属性设置为默认值，并进行返回
    #     """
    #     # 打印出属性的名称
    #     print("get attribute item:{}".format(item))
    #
    #     try:
    #         # 调用父类的方法，如果父类中属性不存在，则抛出异常。
    #         return super().__getattribute__(item)
    #     except AttributeError as e:
    #         print(e)
    #         # python 对象采用字典的方式存储。如果捕获到属性不存在的异常。则通过 __dict__ 写入到对象字典中
    #         self.__dict__[item] = 100
    #         return 100


def main():
    human = Human()
    var = human.age
    print(human.shape)
    # print(human.name)
    # human.name = 'lisi'
    # print(human.name)

    # 输出：{'_Human__name': 'lisi'}
    # 使用 setter 并没有真正意义上的修改，而是更改了名字。 如上: _Human__name
    print(human.__dict__)


if __name__ == '__main__':
    main()
