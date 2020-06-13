# プロトタイプ

from dataclasses import dataclass
# from tkinter import *
import tkinter
import random
import time

tk = tkinter.Tk()
tk.title("電車内混雑シミュレーション")
# tk.state("zoomed")  # ウィンドウの最大化
canvas = tkinter.Canvas(tk, width=790, height=510)
canvas.pack()


@dataclass
class Passenger:
    id: int
    x: int  # 中心を原点にしたときの座標
    y: int
    direction: str  # "Up" / "Down" / "Left" / "Right"
    get_off_station: int  # 降車駅までの残り
    status: str  # "Get on" / "Get off"/ "Wait"
    # age: int
    # gender: str  # "Male" / "Female"

    # 以下は初期化が必要な変数
    tx: int = 0  # 着席の際の目標座標
    ty: int = 0

    def forward(self):
        if self.status != "Wait":
            if self.direction == "Up":
                self.y -= 1
            elif self.direction == "Down":
                self.y += 1
            elif self.direction == "Left":
                self.x -= 1
            elif self.direction == "Right":
                self.x += 1
        else:
            print("pass")
            pass

    def move(self, cv: canvas):
        if self.status == "Get on":
            if -1 <= self.y <= 1:
                nearest_seat(agents, seats)
                if self.x-self.tx > 0:
                    self.direction = "Left"
                    self.forward()
                elif self.x-self.tx < 0:
                    self.direction = "Right"
                    self.forward()
                elif self.x == self.tx:
                    if self.y == self.ty:
                        self.status = "Wait"
                    elif self.y-self.ty > 0:
                        self.direction = "Up"
                        self.forward()
                    elif self.y-self.ty < 0:
                        self.direction = "Down"
                        self.forward()
            else:
                if self.y > 0:
                    if self.x == self.tx and self.y == self.ty:
                        self.status="Wait"
                    else:
                        self.direction = "Up"
                        self.forward()
                else:
                    if self.x == self.tx and self.y == self.ty:
                        self.status="Wait"
                    else:
                        self.direction = "Down"
                        self.forward()

        elif self.status == "Get off":
            if self.y > 0:
                self.direction = "Up"
            else:
                self.direction = "Down"
            self.forward()
        elif self.status == "Wait":
            print(f"{self.id}:{self.status}")
            pass
            # if self.y > 0:
            #     self.direction = "Up"
            # else:
            #     self.direction = "Down"
        if self.x==self.tx and self.y==self.ty:
            self.status="Wait"
        else:
            if -2 <= self.y <= 2:
                self.status = "Get on"

            else:
                self.status = "Get off"
        try:
            canvas.delete(f"P{self.id}")
            if -12 <= self.y <= 12:
                canvas.create_oval(5+20*convertX(self.x), 5+20*convertY(self.y), 5+20*convertX(self.x+1),
                            5+20*convertY(self.y+1), fill="green", tag=f"P{self.id}")
        except Exception as identifier:
            pass
        print(self)


@dataclass
class Seat:
    id: int
    x: int
    y: int
    is_available: bool
    is_priority: bool

# 車内：(0, 10)~(39, 14)
# 座席の座標
# (6, 10)~(12, 10), (16, 10)~(22, 10), (26, 10)~(32, 10)
# (6, 14)~(12, 14), (16, 14)~(22, 14), (26, 14)~(32, 14)
# 優先席の座標
# (0, 10)~(3, 10), (36, 10)~(39, 10), (0, 14)~(3, 14), (36, 14)~(39, 14)

# E233系 乗車定員(座席定員)：160 (54)


# 初期描画 枠線
def create_cells(cv: canvas):
    for i in range(40):
        cv.create_line(5+20*i, 5, 5+20*i, 505)
    for i in range(26):
        cv.create_line(5, 5+20*i, 785,  5+20*i)


# 座席配置
def create_seat(cv: canvas):
    cv.create_rectangle(5, 5+20*10, 5+20*39, 5+20*15, fill="cyan")
    for s in seats:
        if s.is_priority == True:
            cv.create_rectangle(5+20*(convertX(s.x)), 5+20*(convertY(s.y)),
                                5+20*(convertX(s.x)+1), 5+20*(convertY(s.y)+1), fill="yellow")
        else:
            cv.create_rectangle(5+20*(convertX(s.x)), 5+20*(convertY(s.y)),
                                5+20*(convertX(s.x)+1), 5+20*(convertY(s.y)+1), fill="gray")


def check(person: Passenger):
    for p in person:
        if p.x==p.tx and p.y==p.ty:
            p.status="Wait"
        else:
            if -2 <= p.y <= 2:
                p.status = "Get on"

            else:
                p.status = "Get off"

# 指定した座標がマップの中か


def inMap(x, y):
    if -19 <= x <= 19 and -12 <= y <= 12:
        return True
    else:
        return False

# 一番近い座席を見つける


def nearest_seat(person: Passenger, st: Seat):
    for i in person:
        if -1 <= i.y <= 1:
            c = {}  # 座席の候補
            for s in st:
                if s.is_available == True:
                    c[s.id] = abs((i.x)-(s.x))+abs((i.y)-(s.y))
            inv_c = inverse_dict(c)
            target = min(c.values())  # 最も近い座席のid
            i.tx = seats[inv_c[target]].x
            i.ty = seats[inv_c[target]].y

# 参考：https://techacademy.jp/magazine/19140


def inverse_dict(d):
    return {v: k for k, v in d.items()}


def genaratePassenger():
    pass


FIELD_X = 40
FIELD_Y = 40


agents = [
    Passenger(0, 5,  -9, "Up", 5, "Get off"),
    Passenger(1, 15, 10, "Down", 5, "Get off"),
    Passenger(2, -15, 11, "Down", 5, "Get off"),
    Passenger(3, -5, -12, "Down", 5, "Get off"),

]

seats = []
s_idx = 0
for i in range(2):
    for j in range(2):
        # 優先席
        seats.append(Seat(s_idx, (-19)*(-1)**i, (-2)*(-1)**j, True, True))
        s_idx += 1
        seats.append(Seat(s_idx, (-18)*(-1)**i, (-2)*(-1)**j, True, True))
        s_idx += 1
        seats.append(Seat(s_idx, (-17)*(-1)**i, (-2)*(-1)**j, True, True))
        s_idx += 1

        # 座席
        seats.append(Seat(s_idx, (-13)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-12)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-11)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-10)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-9)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-8)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-7)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1

        seats.append(Seat(s_idx, (-3)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-2)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
        seats.append(Seat(s_idx, (-1)*(-1)**i, (-2)*(-1)**j, True, False))
        s_idx += 1
    seats.append(Seat(s_idx, 0, (-2)*(-1)**i, True, False))
    s_idx += 1

train = []


def drawPassenger(person: Passenger, cv: canvas):
    try:
        cv.delete(f"P{person.id}")
        if -12 <= person.y <= 12:
            cv.create_oval(5+20*convertX(person.x), 5+20*convertY(person.y), 5+20*convertX(person.x+1),
                           5+20*convertY(person.y+1), fill="green", tag=f"P{person.id}")
    except Exception as identifier:
        pass


# <!-- デバッグ用関数
# 左上原点から中心を原点に変換
def convertX(orig_X: int):
    return orig_X+19


def convertY(orig_Y: int):
    return orig_Y+12
# デバッグ用関数 ここまで-->


def main():
    # check(agents)
    for a in agents:
    # if a.status != "Wait":
        a.move(canvas)
            # drawPassenger(a, canvas)
    #tk.after(100, main)


create_seat(canvas)
create_cells(canvas)

while True:
    main()
    time.sleep(0.5)
    try:
        tk.update()
    except Exception as identifier:
        exit(0)


tk.mainloop()
