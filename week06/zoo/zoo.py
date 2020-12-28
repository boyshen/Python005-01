# -*- encoding: utf-8 -*-
"""
@file: zoo.py
@time: 2020/12/27 下午6:36
@author: shenpinggang
@contact: 1285456152@qq.com
@desc: 
"""
from collections import defaultdict
from abc import ABCMeta, abstractmethod

DOG = 'dog'
CAT = 'cat'


class Zoo(object):
    """
    动物园类
    """

    def __init__(self, name):
        # 名字属性
        self.name = name

        # 根据动物品种保存动物实例
        self.animal_type = defaultdict(set)

    def add_animal(self, animal):
        """
        添加动物
        :param animal: (object)
        :return: (bool)
        """
        # 不允许重复添加动物实例
        if animal in self.animal_type[animal.animal_type]:
            print("Instance already exists! {} ".format(animal))
            return False
        self.animal_type[animal.animal_type].add(animal)
        return True

    def has_animal(self, animal_type, animal_name=None):
        """
        是否有该类型动物
        :return: (list) 动物对象
        """
        animal_type = animal_type.lower()
        animals = self.animal_type[animal_type]
        if len(animals) != 0 and animal_name is not None:
            result = [animal for animal in animals if animal.name == animal_name]
        else:
            result = list(animals)
        return result

    def __repr__(self):
        animal_type = [a_type for a_type in self.animal_type.keys()]
        return "<名字：{name}, 动物种类：{animal_type}>".format(name=self.name, animal_type=animal_type)


class Animal(metaclass=ABCMeta):
    """
    动物类（抽象类，不允许实例化）
    """
    SHAPE_LARGE = 2
    SHAPE_SECONDARY = 1
    SHAPE_SMALL = 0

    TYPE_MEAT = "meta"
    TYPE_GRASS = "grass"

    CHARACTER_FEROCIOUS = "ferocious"
    CHARACTER_MEEKNESS = "meekness"

    def __init__(self, _type, _shape, _character):
        self.__type = _type
        self.__shape = _shape
        self.__character = _character

        self.__animal_type = {Animal.TYPE_MEAT: "食肉", Animal.TYPE_GRASS: "食草"}
        self.__animal_character = {Animal.CHARACTER_FEROCIOUS: "凶猛", Animal.CHARACTER_MEEKNESS: "温和"}
        self.__animal_shape = {Animal.SHAPE_LARGE: "大", Animal.SHAPE_SECONDARY: "中", Animal.SHAPE_SMALL: "小"}

    @property
    def type_(self):
        """
        类型
        :return:
        """
        return self.__animal_type[self.__type]

    @property
    def shape_(self):
        """
        体型
        :return:
        """
        return self.__animal_shape[self.__shape]

    @property
    def character_(self):
        """
        性格
        :return:
        """
        return self.__animal_character[self.__character]

    @property
    def is_fierce(self):
        """
        是否凶猛
        :return:
        """
        if self.__shape >= Animal.SHAPE_SECONDARY \
                and self.__type == Animal.TYPE_MEAT \
                and self.__character == Animal.CHARACTER_FEROCIOUS:
            return True
        return False

    @abstractmethod
    def __repr__(self):
        pass


class Cat(Animal):
    """
    猫类 (继承 Animal)
    """
    # 叫声。类属性
    calls = 'Meow'

    def __init__(self, name, _type, _shape, _character):
        super(Cat, self).__init__(_type, _shape, _character)
        self.name = name
        self.__animal_type = CAT

    @property
    def is_pets(self):
        """
        是否适合做宠物
        :return: (bool)
        """
        if self.is_fierce:
            return False
        return True

    @property
    def animal_type(self):
        return self.__animal_type

    def __repr__(self):
        return "<名字：{name}, " \
               "种类：{animal_type}, " \
               "类型：{type_}, " \
               "体型：{shape}, " \
               "性格：{character}, " \
               "是否凶猛：{is_fierce}, " \
               "是否适合做宠物：{is_pets}, " \
               "叫声：{calls}>".format(name=self.name,
                                    animal_type=self.animal_type,
                                    type_=self.type_,
                                    shape=self.shape_,
                                    character=self.character_,
                                    is_fierce=self.is_fierce,
                                    is_pets=self.is_pets,
                                    calls=Cat.calls)


class Dog(Animal):
    """
    狗类 (继承 Animal)
    """
    calls = 'Wang'

    def __init__(self, name, _type, _shape, _character):
        super(Dog, self).__init__(_type, _shape, _character)
        self.name = name
        self.__animal_type = DOG

    @property
    def is_pets(self):
        """
        是否适合做宠物
        :return: (bool)
        """
        if self.is_fierce:
            return False
        return True

    @property
    def animal_type(self):
        return self.__animal_type

    def __repr__(self):
        return "<名字：{name}, " \
               "种类：{animal_type}, " \
               "类型：{type_}, " \
               "体型：{shape}, " \
               "性格：{character}, " \
               "是否凶猛：{is_fierce}, " \
               "是否适合做宠物：{is_pets}, " \
               "叫声：{calls}>".format(name=self.name,
                                    animal_type=self.animal_type,
                                    type_=self.type_,
                                    shape=self.shape_,
                                    character=self.character_,
                                    is_fierce=self.is_fierce,
                                    is_pets=self.is_pets,
                                    calls=Dog.calls)


def main():
    # a = Animal(1, 2, 3)
    zoo = Zoo("时间动物园")

    cat1 = Cat('大花猫', Animal.TYPE_MEAT, Animal.SHAPE_SMALL, Animal.CHARACTER_MEEKNESS)
    zoo.add_animal(cat1)
    print(cat1)

    cat2 = Cat('大白猫', Animal.TYPE_MEAT, Animal.SHAPE_SMALL, Animal.CHARACTER_MEEKNESS)
    zoo.add_animal(cat2)
    print(cat2)

    dog1 = Dog('狗', Animal.TYPE_MEAT, Animal.SHAPE_SMALL, Animal.CHARACTER_MEEKNESS)
    zoo.add_animal(dog1)
    print(dog1)

    dog2 = Dog('大狗', Animal.TYPE_MEAT, Animal.SHAPE_SECONDARY, Animal.CHARACTER_FEROCIOUS)
    zoo.add_animal(dog2)
    print(dog2)

    print(zoo)

    # 搜索动物
    result = zoo.has_animal('Cat')
    for animal in result:
        print("找到猫：{}".format(animal))

    result = zoo.has_animal('Dog', '大狗')
    for animal in result:
        print("找到狗：{}".format(animal))


if __name__ == '__main__':
    main()
