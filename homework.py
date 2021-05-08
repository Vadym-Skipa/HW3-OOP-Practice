from abc import ABC, abstractmethod
import random


class HouseAbstract(ABC):
    @abstractmethod
    def area(self):
        raise NotImplementedError(f"class - {self.__class__}, property - area")

    @abstractmethod
    def cost(self):
        raise NotImplementedError(f"class - {self.__class__}, property - area")

    def __str__(self):
        return f"It's {self.__class__}: its area is {self.area} and its cost is {self.cost}"

    def __repr__(self):
        return self.__str__()


class HouseForSaleAbstract(HouseAbstract):
    @abstractmethod
    def apply_discount(self, discount: int):
        raise NotImplementedError(f"class - {self.__class__}, method - apply_discount")


class House(HouseForSaleAbstract):
    def __init__(self, area: int, cost: int):
        self._area = area
        self._cost = cost

    @property
    def area(self):
        return self._area

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost: int):
        self._cost = max(0, cost)

    def apply_discount(self, discount: int):
        self._cost -= discount


class SmallTypicalHouse(HouseForSaleAbstract):
    def __init__(self, cost: int):
        self._cost = cost

    @property
    def area(self):
        return 40

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, cost: int):
        self._cost = max(0, cost)

    def apply_discount(self, discount: int):
        self._cost -= discount


class RealtorSingletonMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if not cls._instance:
            instance = super().__call__(*args, **kwargs)
            cls._instance = instance
        return cls._instance


class Realtor(metaclass=RealtorSingletonMeta):
    def __init__(self, name: str, houses: list, possible_discount: int):
        self.name = name
        self._houses = houses
        self._discount = possible_discount

    def info(self):
        if self._houses:
            print("Available houses:")
            for house in self._houses:
                print(f"\t{house}")
        else:
            print("No available houses:")
        return self._houses

    def give_discount(self, house: HouseAbstract):
        if house in self._houses:
            house: HouseForSaleAbstract
            house.apply_discount(self._discount)

    def sale_house(self, house: HouseAbstract, money: int):
        if house in self._houses and money >= house.cost:
            if random.random() >= 0.1:
                self._houses.remove(house)
                return house


class NotEnoughMoneyException(Exception):
    pass


class Person(ABC):
    def __init__(self, name: str, age: int, money: int = 0, houses: list = None):
        self.name = name
        self._age = age
        self._money = money
        self._houses = houses

    @property
    def age(self):
        return self._age

    @property
    def money(self):
        return self._money

    @property
    def houses(self):
        return self._houses

    def info(self):
        print(self)

    def __str__(self):
        return f"I am {self.__class__}, my name is {self.name}, my age is {self._age}"

    @abstractmethod
    def make_money(self):
        raise NotImplementedError(f"class - {self.__class__}, method - make_money")

    def _give_money(self, money: int):
        if money <= self._money:
            self._money -= money
            return money
        raise NotEnoughMoneyException

    def _append_house(self, house: HouseAbstract):
        if self._houses:
            self._houses.append(house)
        else:
            self._houses = [house]

    def buy_house(self, house: HouseAbstract, ask_for_discount: bool = False):
        if ask_for_discount:
            Realtor().give_discount(house)
        money = self._give_money(house.cost)
        purchase = Realtor().sale_house(house, money)
        if purchase:
            self._append_house(house)


class RegularEmployee(Person):
    def __init__(self, name: str, age: int, salary: int, money: int = 0, houses: list = None):
        super().__init__(name, age, money, houses)
        self._salary = salary

    def make_money(self):
        self._money += self._salary

    def __str__(self):
        return super().__str__() + f", my salary is {self._salary}"


class Freelancer(Person):
    def __init__(self, name: str, age: int, average_revenue: int, money: int = 0, houses: list = None):
        super().__init__(name, age, money, houses)
        self._average_revenue = average_revenue

    def make_money(self):
        self._money += random.randrange(0, self._average_revenue * 2 + 1)

    def __str__(self):
        return super().__str__() + f", my average revenue is {self._average_revenue}"


if __name__ == "__main__":
    def work_and_buy(worker: Person, house: HouseAbstract, disc: bool):
        while(True):
            try:
                worker.buy_house(house, disc)
            except NotEnoughMoneyException:
                worker.make_money()
                print(f"{worker.name} has ${worker.money}")
            else:
                print(f"{worker.name} has {worker.houses} and ${worker.money}")
                break

    reg_emp = RegularEmployee("John", 28, 2000)
    freel = Freelancer("Bill", 23, 2000)
    house1 = House(50, 5000)
    house2 = House(100, 15000)
    house3 = House(67, 23000)
    houses = [house1, house2, house3]
    houses += [SmallTypicalHouse(6500), SmallTypicalHouse(3000), SmallTypicalHouse(8000)]
    realtor = Realtor("Steve", houses, 200)
    realtor.info()
    work_and_buy(reg_emp, houses[3], True)
    work_and_buy(reg_emp, houses[1], False)
    work_and_buy(freel, houses[2], True)
    realtor.info()
