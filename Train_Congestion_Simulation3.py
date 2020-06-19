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


FIELD_X = 40
FIELD_Y = 40
TURN_MOVING = 25  # 停車から発車までにエージェントが動けるマス
t_m = TURN_MOVING


@dataclass
class Passenger:
    id: int
    x: int  # 中心を原点にしたときの座標
    y: int
    direction: str  # "Up" / "Down" / "Left" / "Right"
    get_off_station: int  # 降車駅までの残り
    status: str  # "Get on" / "Get off" / "Wait"
    # age: int
    # gender: str  # "Male" / "Female"

    # 以下は初期化が必要な変数
    tx: int = 0  # 着席の際の目標座標
    ty: int = 0


def forward(person):
    if person.status != "Wait":
        if person.direction == "Up":
            person.y -= 1
        elif person.direction == "Down":
            person.y += 1
        elif person.direction == "Left":
            person.x -= 1
        elif person.direction == "Right":
            person.x += 1
    else:
        print("pass")
        pass


def move(passengers, cv: canvas):
    for person in passengers:
        if train[0] == "Stop":
            try:
                canvas.delete(f"P{person.id}")
                if -12 <= person.y <= 12:
                    canvas.create_oval(5+20*convertX(person.x), 5+20*convertY(person.y), 5+20*convertX(person.x+1),
                                       5+20*convertY(person.y+1), fill="green", tag=f"P{person.id}")
            except Exception as identifier:
                pass
            if person.status == "Get on":
                if person.get_off_station != 0:
                    # 乗車
                    if -1 <= person.y <= 1:
                        nearest_seat(agents, seats)
                        if person.x-person.tx > 0:
                            person.direction = "Left"
                            forward(person)
                        elif person.x-person.tx < 0:
                            person.direction = "Right"
                            forward(person)
                        elif person.x == person.tx:
                            if person.y == person.ty:
                                person.status = "Wait"
                                seats[get_seat_id(person)].is_available = False
                            elif person.y-person.ty > 0:
                                person.direction = "Up"
                                forward(person)
                            elif person.y-person.ty < 0:
                                person.direction = "Down"
                                forward(person)
                    else:
                        if person.y > 0:
                            if person.x == person.tx and person.y == person.ty:
                                person.status = "Wait"
                                seats[get_seat_id(person)].is_available = False
                            else:
                                person.direction = "Up"
                                forward(person)
                        else:
                            if person.x == person.tx and person.y == person.ty:
                                person.status = "Wait"
                                seats[get_seat_id(person)].is_available = False
                            else:
                                person.direction = "Down"
                                forward(person)
                else:
                    if person.y == 2:
                        if person.tx==person.x:
                            person.direction = "Down"
                        else:                            
                            person.direction = "Up"
                        forward(person)
                    elif person.y == -2:
                        if person.tx==person.x:
                            person.direction = "Up"
                        else:                            
                            person.direction = "Down"
                        forward(person)
                    else:
                        if person.tx-person.x == 0:
                            if person.ty-person.y > 0:
                                person.direction = "Up"
                                forward(person)
                                if person.y <= 2:
                                    person.status = "Get off"
                            else:
                                person.direction = "Down"
                                forward(person)
                                if person.y >= 2:
                                    person.status = "Get off"
                        elif person.tx-person.x > 0:
                            person.direction = "Right"
                            forward(person)
                        elif person.tx-person.x < 0:
                            person.direction = "Left"
                            forward(person)

            elif person.status == "Get off":
                if person.get_off_station!=0: 
                    if person.y > 0:
                        person.direction = "Up"
                    else:
                        person.direction = "Down"
                    forward(person)
                else:
                    if person.y < 0:
                        person.direction = "Up"
                    else:
                        person.direction = "Down"
                    forward(person)
                    
            elif person.status == "Wait":
                # print(f"{person.id}:{person.status}")
                if person.get_off_station == 0:
                    person.status = "Get on"
                    nearest_door(person)
                pass
                # if person.y > 0:
                #     person.direction = "Up"
                # else:
                #     person.direction = "Down"
            if person.x == person.tx and person.y == person.ty:
                person.status = "Wait"
                seats[get_seat_id(person)].is_available = False
            else:
                if -2 <= person.y <= 2:
                    person.status = "Get on"

                else:
                    person.status = "Get off"
            print(person)
            global t_m
            if t_m == 0:
                train[0] = "Move"

        elif train[0] == "Move":
            pass


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
        if p.x == p.tx and p.y == p.ty:
            p.status = "Wait"
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

def get_seat_id(person: Passenger):
    for s in seats:
        if s.x == person.x and s.y == person.y:
            return s.id

def nearest_door(person: Passenger):
    # ドアの座標：(±5, ±2), (±15, ±2) 複合任意
    if -19 <= person.x <= -10:
        person.tx = -15
    elif person.x <= 0:
        person.tx = -5
    elif person.x <= 10:
        person.tx = 5
    elif person.x <= 19:
        person.tx = 15

    if train[1] == "Up":
        person.ty = -20
    elif train[1] == "Down":
        person.ty = 20


def turn(passengers: list):
    for person in passengers:
        person.get_off_station -= 1



def inverse_dict(d):
    return {v: k for k, v in d.items()}


def genaratePassenger():
    pass


agents = [
    Passenger(0, 5,  -9, "Up", 2, "Get off"),
    Passenger(1, 15, 10, "Down", 1, "Get off"),
    Passenger(2, -15, 11, "Down", 3, "Get off"),
    Passenger(3, -5, -12, "Down", 4, "Get off"),

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

train = ["Stop", "Up"]  # [<電車の状態>, <ドアが開く方向>]


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
    # for a in agents:
    # if a.status != "Wait":
    move(agents, canvas)
    global t_m
    t_m -= 1
    print(t_m)
    if t_m == 0:
        turn(agents)
        t_m = TURN_MOVING
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
