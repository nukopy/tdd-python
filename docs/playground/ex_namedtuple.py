from collections import namedtuple


# namedtuple の定義
# 第一引数の name で namedtuple が作られる．そのため，変数名を第一引数に合わせないとコードが読みづらくなる．
# * 省メモリな immutable なクラス（だと考えれば良い）
# * クラス定義のショートカット（だと考えれば良い）
Car = namedtuple("Car", ["color", "mileage"])
my_car = Car("red", 3812.4)
print(my_car.color, my_car.mileage)


class MyCar(Car):
    # namedtuple を継承してクラスを作れる
    # immutable な属性（attribute）を作成できる
    def hexcolor(self):
        if self.color == "red":
            return "#ff0000"
        else:
            return "#000000"


c1 = MyCar("red", 1234)
c2 = MyCar("blue", 3000)
