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
    status: str  # "Get_on" / "Get_off"/ "Wait"
    # age: int
    # gender: str  # "Male" / "Female"

    # 以下は初期化が必要な変数
    tx: int = 0  # 着席の際の目標座標
    ty: int = 0

    def forward(self):
        if self.direction == "Up":
            self.y -= 1
        elif self.direction == "Down":
            self.y += 1
        elif self.direction == "Left":
            self.x -= 1
        elif self.direction == "Right":
            self.x += 1

    def move(self, cv: canvas):
        if self.status == "Get_on":
            pass
        else:
            pass
            # if self.y > 0:
            #     self.direction = "Up"
            # else:
            #     self.direction = "Down"
        self.forward()


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
        cv.create_rectangle(5+20*(convertX(s.x)), 5+20*(convertY(s.y)),
                            5+20*(convertX(s.x)+1), 5+20*(convertY(s.y)+1), fill="gray")

    # for i in range(2):
    #     for j in range(2):
    #         print(f"{convertX((-19)*(-1)**i)}, {convertY((-2))} -> {convertX((-16)*(-1)**i)}, {convertY((-1))}")
    #         cv.create_rectangle(5+20*convertX((-9)*(-1)**i), 5+20*convertY((-2)*(-1)**j),
    #                             5+20*convertX((-16)*(-1)**i), 5+20*convertY((-1)*(-1)**j), fill="yellow")

    # cv.create_rectangle(5, 5+20*10, 5+20*3, 5+20*11, fill="yellow")
    # cv.create_rectangle(5, 5+20*14, 5+20*3, 5+20*15, fill="yellow")
    # cv.create_rectangle(5+20*6, 5+20*10, 5+20*13, 5+20*11, fill="gray")
    # cv.create_rectangle(5+20*6, 5+20*14, 5+20*13, 5+20*15, fill="gray")
    # cv.create_rectangle(5+20*16, 5+20*10, 5+20*23, 5+20*11, fill="gray")
    # cv.create_rectangle(5+20*16, 5+20*14, 5+20*23, 5+20*15, fill="gray")
    # cv.create_rectangle(5+20*26, 5+20*10, 5+20*33, 5+20*11, fill="gray")
    # cv.create_rectangle(5+20*26, 5+20*14, 5+20*33, 5+20*15, fill="gray")
    # cv.create_rectangle(5+20*36, 5+20*10, 5+20*39, 5+20*11, fill="yellow")
    # cv.create_rectangle(5+20*36, 5+20*14, 5+20*39, 5+20*15, fill="yellow")


def check(person: Passenger):
    for p in person:
        if -2 <= p.y <= 2:
            p.in_train = True


def nearest_seat(person: Passenger, st: Seat):
    for i in person:
        if -1 <= i.y <= 1:
            c = {}  # 座席の候補
            for s in st:
                c[s.id] = abs((i.x)-(s.x))+abs((i.y)-(s.y))


def genaratePassenger():
    pass


FIELD_X = 40
FIELD_Y = 40


agents = [
    Passenger(0, 5,  9, "Up", 5, "Get_off"),
    Passenger(1, 15, -9, "Down", 5, "Get_off"),
    Passenger(2, -5, 4, "Left", 5, "Get_off"),
    Passenger(3, -2, 10, "Right", 5, "Get_off"),

]

seats = [
    # Seat(0, -19, -2, True, True),
    # Seat(1, -18, -2, True, True),
    # Seat(2, -17, -2, True, True),
    # Seat(3, -19, 2, True, True),
    # Seat(4, -18, 2, True, True),
    # Seat(5, -17, 2, True, True),
    # Seat(6, 19, -2, True, True),
    # Seat(7, 18, -2, True, True),
    # Seat(8, 17, -2, True, True),
    # Seat(9, 19, 2, True, True),
    # Seat(10, 18, 2, True, True),
    # Seat(11, 17, 2, True, True),

    # Seat(12, -13, -2, True, False),
    # Seat(13, -12, -2, True, False),
    # Seat(14, -11, -2, True, False),
    # Seat(15, -10, -2, True, False),
    # Seat(16, -9, -2, True, False),
    # Seat(17, -8, -2, True, False),
    # Seat(18, -7, -2, True, False),

]

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
        seats.append(Seat(s_idx, 0, (-2)*(-1)**j, True, False))
        s_idx += 1


train = []


def drawPassenger(PassengerList: list, cv: canvas):
    for p in PassengerList:
        try:
            cv.delete(f"P{p.id}")
            if -12 <= p.y <= 12:
                cv.create_oval(5+20*convertX(p.x), 5+20*convertY(p.y), 5+20*convertX(p.x+1),
                               5+20*convertY(p.y+1), fill="green", tag=f"P{p.id}")
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
    drawPassenger(agents, canvas)
    for a in agents:
        a.move(canvas)
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
