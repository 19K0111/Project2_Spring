# プロトタイプ

from dataclasses import dataclass
# from tkinter import *
import tkinter
import random
import time
import matplotlib.pyplot as plt
import numpy as np

tk = tkinter.Tk()
tk.title("電車内混雑シミュレーション")
# tk.state("zoomed")  # ウィンドウの最大化
canvas = tkinter.Canvas(tk, width=790, height=510)
canvas.pack()


fig = plt.figure()
ax1 = fig.add_subplot(3, 2, 1)  # 車内の乗客数
ax1.grid()
ax2 = fig.add_subplot(3, 2, 2)  # ストレス度合(1駅)
ax2.grid()
ax3 = fig.add_subplot(3, 2, 3)  # ストレス度合(2駅)
ax3.grid()
ax4 = fig.add_subplot(3, 2, 4)  # ストレス度合(3駅)
ax4.grid()
ax5 = fig.add_subplot(3, 2, 5)  # ストレス度合(4駅)
ax5.grid()
ax6 = fig.add_subplot(3, 2, 6)  # ストレス度合(5駅)
ax6.grid()

X = -1  # 試行回数
NX = [0]
cur = 0  # 乗客数
NY = [0]
FIELD_Y = 40
TURN_MOVING = 40  # 停車から発車までにエージェントが動けるマス
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
    _GET_OFF_STATION: int = -1
    stress: float = 0.0  # ストレス度合(0~100)


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
                if -12 <= person.y <= 12 and -19 <= person.x <= 19:
                    canvas.create_oval(5+20*convertX(person.x), 5+20*convertY(person.y), 5+20*convertX(person.x+1),
                                       5+20*convertY(person.y+1), fill="green", tag=f"P{person.id}")
            except Exception:  # as identifier:
                pass
            if person.status == "Get on":
                if person.get_off_station != 0:
                    # 乗車
                    if -1 <= person.y <= 1:
                        # 座席に向かう
                        nearest_seat(person, seats)
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
                            # 座席の手前
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
                    # 下車する人の動き
                    if person.y == 2:
                        if person.tx == person.x:
                            # person.direction = "Down"
                            pass
                        else:
                            person.direction = "Up"
                        forward(person)
                    elif person.y == -2:
                        if person.tx == person.x:
                            # person.direction = "Up"
                            pass
                        else:
                            person.direction = "Down"
                        forward(person)
                    else:
                        if person.tx-person.x == 0:
                            if person.ty > 0:
                                person.direction = "Down"
                                forward(person)
                                if person.y <= 2:
                                    person.status = "Get off"
                            else:
                                # elif person.x==-15 or person.x==-5 or person.x==5 or person.x ==15 and person.ty-person.y <= 0:
                                person.direction = "Up"
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
                if person.get_off_station != 0:
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
                    seats[get_seat_id(person)].is_available = True
                    nearest_door(person)
                pass
                # if person.y > 0:
                #     person.direction = "Up"
                # else:
                #     person.direction = "Down"
            if person.x == person.tx and person.y == person.ty and person.get_off_station != 0:
                person.status = "Wait"
                seats[get_seat_id(person)].is_available = False
            else:
                if -2 <= person.y <= 2:
                    person.status = "Get on"

                else:
                    person.status = "Get off"
                if person.y > 15 or person.y < -15:
                    person.status = "Done"
                    # break
            # print(person)
            # global t_m
            # if t_m == 0:
            #     train[0] = "Move"
            #     train[1] = random.choice(("Up", "Down"))

        elif train[0] == "Move":
            # 新たに乗車するエージェントを配置
            try:
                canvas.delete(f"P{person.id}")
                if -12 <= person.y <= 12 and -19 <= person.x <= 19:
                    canvas.create_oval(5+20*convertX(person.x), 5+20*convertY(person.y), 5+20*convertX(person.x+1),
                                       5+20*convertY(person.y+1), fill="green", tag=f"P{person.id}")
            except Exception:  # as identifier:
                pass

            if person.status == "Get_off":
                forward(person)

            pass
            # if t_m == 0:
            #     train[0] = "Stop"
            # pass
        print(person)

    # forを抜けた
    global cur
    cur = 0
    for pp in agents:
        if pp.status == "Get_on" or pp.status == "Wait":
            cur += 1
    print(f"乗客数：{cur}人")
    global t_m
    if t_m == 0 and train[0] == "Stop":
        train[0] = "Move"
        train[1] = random.choice(("Up", "Down"))
        generatePassenger(agents)
    elif t_m == 0 and train[0] == "Move":
        train[0] = "Stop"


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
    # for i in person:
    if -1 <= person.y <= 1:
        c = {}  # 座席の候補
        for s in st:
            if s.is_available == True:
                # 座席の候補と座席までの距離を結びつける
                c[s.id] = abs((person.x)-(s.x))+abs((person.y)-(s.y))
                # 候補の座席の隣に座っているか
                try:  # 端の座席の一方は
                    if st[get_seat_id_by_coordinates(s.x-1, s.y)].is_available == False or st[get_seat_id_by_coordinates(s.x+1, s.y)].is_available == False:
                        c[s.id] += 10
                except:
                    pass

        inv_c = inverse_dict(c)
        try:  # 満員のとき、座席がなくなりエラーが発生
            target = min(c.values())  # 最も近い座席のid
            person.tx = seats[inv_c[target]].x
            person.ty = seats[inv_c[target]].y
            pass
        except Exception:
            pass


# 座席の評価関数
def evaluate(person: Passenger, st: Seat):
    # 座席が端 -> 評価高め
    pass


def get_seat_id(person: Passenger):
    for s in seats:
        if s.x == person.x and s.y == person.y:
            return s.id


# 座標から座席idを取得
def get_seat_id_by_coordinates(x: int, y: int):
    for s in seats:
        if s.x == x and s.y == y:
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
        person.ty = -15
    elif train[1] == "Down":
        person.ty = 15


def turn(passengers: list):
    for person in passengers:
        if person.status != "Done":
            person.get_off_station -= 1
            person._GET_OFF_STATION += 1
            calc_stress(person)


def inverse_dict(d):
    # 参考：https://techacademy.jp/magazine/19140
    return {v: k for k, v in d.items()}


def generatePassenger(passengers: list):
    if train[1] == "Up":
        g1 = random.randint(0, 5)
        for i1 in range(g1):
            passengers.append(Passenger(
                len(passengers), -15+TURN_MOVING, -5-i1, "Left", random.randint(2, 6), "Get_off"))
        g2 = random.randint(0, 5)
        for i2 in range(g2):
            passengers.append(Passenger(
                len(passengers), -5+TURN_MOVING, -5-i2, "Left", random.randint(2, 6), "Get_off"))
        g3 = random.randint(0, 5)
        for i3 in range(g3):
            passengers.append(Passenger(
                len(passengers), 5+TURN_MOVING, -5-i3, "Left", random.randint(2, 6), "Get_off"))
        g4 = random.randint(0, 5)
        for i4 in range(g4):
            passengers.append(Passenger(
                len(passengers), 15+TURN_MOVING, -5-i4, "Left", random.randint(2, 6), "Get_off"))
        pass
    elif train[1] == "Down":
        g1 = random.randint(0, 5)
        for i1 in range(g1):
            passengers.append(Passenger(
                len(passengers), -15+TURN_MOVING, 5+i1, "Left", random.randint(2, 6), "Get_off"))
        g2 = random.randint(0, 5)
        for i2 in range(g2):
            passengers.append(Passenger(
                len(passengers), -5+TURN_MOVING, 5+i2, "Left", random.randint(2, 6), "Get_off"))
        g3 = random.randint(0, 5)
        for i3 in range(g3):
            passengers.append(Passenger(
                len(passengers), 5+TURN_MOVING, 5+i3, "Left", random.randint(2, 6), "Get_off"))
        g4 = random.randint(0, 5)
        for i4 in range(g4):
            passengers.append(Passenger(
                len(passengers), 15+TURN_MOVING, 5+i4, "Left", random.randint(2, 6), "Get_off"))
        pass

    pass


# 周囲にいる人の有無でストレスを計算
def calc_stress(person: Passenger):
    if person.status == "Get on" or person.status == "Wait":
        if person.stress >= 0.0:
            for p in agents:
                if p.y-1 <= person.y <= p.y+1 and p.x-1 <= person.x <= p.x+1 and person.id != p.id:
                    # 着席しているか否かで分岐
                    if person.y == -2 or person.y == 2:
                        if abs(person.x) == 19 or abs(person.x) == 17 or abs(person.x) == 13 or abs(person.x) == 7 or abs(person.x) == 3:
                            person.stress += 3
                        else:
                            person.stress += 7
                    else:
                        person.stress += 10
            pass
        else:
            person.stress = 0.0
        person.stress = round(person.stress, 2)
        pass


# グラフ化
def show_graph():
    global X, cur, NX, NY
    # 現在の乗客数を描画
    NX.append(X)
    NY.append(cur)

    # fig.delaxes(ax1)
    # fig.delaxes(ax2)
    # fig.delaxes(ax3)
    # fig.delaxes(ax4)
    # fig.delaxes(ax5)
    # fig.delaxes(ax6)

    l1,=ax1.plot(NX, NY)
    ax1.set_xlim(0, max([max(NX), 50]))
    ax1.set_ylim(0, max([max(NY), 60]))
    ax1.set_xlabel("試行回数(回)", fontname="MS Gothic")
    ax1.set_ylabel("乗客数(人)", fontname="MS Gothic")
    ax1.set_title(f"車内にいる乗客数(累計{len(agents)}人)", fontname="MS Gothic")

    p1=ax2.scatter([i for i in range(len(G1))], G1)
    ax2.set_ylim(0,100)
    ax2.set_ylabel("ストレス度合(%)", fontname="MS Gothic")
    ax2.set_title("1駅で降りる人のストレス度合", fontname="MS Gothic")

    p2=ax3.scatter([i for i in range(len(G2))], G2)
    ax3.set_ylim(0,100)
    ax3.set_ylabel("ストレス度合(%)", fontname="MS Gothic")
    ax3.set_title("2駅で降りる人のストレス度合", fontname="MS Gothic")

    p3=ax4.scatter([i for i in range(len(G3))], G3)
    ax4.set_ylim(0,100)
    ax4.set_ylabel("ストレス度合(%)", fontname="MS Gothic")
    ax4.set_title("3駅で降りる人のストレス度合", fontname="MS Gothic")

    p4=ax5.scatter([i for i in range(len(G4))], G4)
    ax5.set_ylim(0,100)
    ax5.set_ylabel("ストレス度合(%)", fontname="MS Gothic")
    ax5.set_title("4駅で降りる人のストレス度合", fontname="MS Gothic")

    p5=ax6.scatter([i for i in range(len(G5))], G5)
    ax6.set_ylim(0,100)
    ax6.set_ylabel("ストレス度合(%)", fontname="MS Gothic")
    ax6.set_title("5駅で降りる人のストレス度合", fontname="MS Gothic")

    fig.tight_layout()
    plt.pause(0.001)
    l1.remove()
    p1.remove()
    p2.remove()
    p3.remove()
    p4.remove()
    p5.remove()
    pass


agents = [
    # Passenger(0, 5, 5, "Up", 1, "Get off"),
    # Passenger(1, 5, 6, "Up", 2, "Get off"),
    # Passenger(2, 5, 7, "Up", 3, "Get off"),
    # Passenger(3, 5, 8, "Up", 1, "Get off"),
    # Passenger(4, 5, 9, "Up", 2, "Get off"),
    # Passenger(5, 5, 10, "Up", 3, "Get off"),
    # Passenger(6, 5, 11, "Up", 1, "Get off"),

    # Passenger(7, 15, 5, "Up", 1, "Get off"),
    # Passenger(8, 15, 6, "Up", 2, "Get off"),
    # Passenger(9, 15, 7, "Up", 3, "Get off"),
    # Passenger(10, 15, 8, "Up", 1, "Get off"),
    # Passenger(11, 15, 9, "Up", 2, "Get off"),
    # Passenger(12, 15, 10, "Up", 3, "Get off"),
    # Passenger(13, 15, 11, "Up", 1, "Get off"),

    # Passenger(14, -5, 5, "Up", 1, "Get off"),
    # Passenger(15, -5, 6, "Up", 2, "Get off"),
    # Passenger(16, -5, 7, "Up", 3, "Get off"),
    # Passenger(17, -5, 8, "Up", 1, "Get off"),
    # Passenger(18, -5, 9, "Up", 2, "Get off"),
    # Passenger(19, -5, 10, "Up", 3, "Get off"),
    # Passenger(20, -5, 11, "Up", 1, "Get off"),

    # Passenger(21, -15, 5, "Up", 1, "Get off"),
    # Passenger(22, -15, 6, "Up", 2, "Get off"),
    # Passenger(23, -15, 7, "Up", 3, "Get off"),
    # Passenger(24, -15, 8, "Up", 1, "Get off"),
    # Passenger(25, -15, 9, "Up", 2, "Get off"),
    # Passenger(26, -15, 10, "Up", 3, "Get off"),
    # Passenger(27, -15, 11, "Up", 1, "Get off"),

    # Passenger(28, 5, -5, "Down", 1, "Get off"),
    # Passenger(29, 5, -6, "Down", 2, "Get off"),
    # Passenger(30, 5, -7, "Down", 3, "Get off"),
    # Passenger(31, 5, -8, "Down", 1, "Get off"),
    # Passenger(32, 5, -9, "Down", 2, "Get off"),
    # Passenger(33, 5, -10, "Down", 3, "Get off"),
    # Passenger(34, 5, -11, "Down", 1, "Get off"),

    # Passenger(35, 15, -5, "Down", 1, "Get off"),
    # Passenger(36, 15, -6, "Down", 2, "Get off"),
    # Passenger(37, 15, -7, "Down", 3, "Get off"),
    # Passenger(38, 15, -8, "Down", 1, "Get off"),
    # Passenger(39, 15, -9, "Down", 2, "Get off"),
    # Passenger(40, 15, -10, "Down", 3, "Get off"),
    # Passenger(41, 15, -11, "Down", 1, "Get off"),

    # Passenger(42, -5, -5, "Down", 1, "Get off"),
    # Passenger(43, -5, -6, "Down", 2, "Get off"),
    # Passenger(44, -5, -7, "Down", 3, "Get off"),
    # Passenger(45, -5, -8, "Down", 1, "Get off"),
    # Passenger(46, -5, -9, "Down", 2, "Get off"),
    # Passenger(47, -5, -10, "Down", 3, "Get off"),
    # Passenger(48, -5, -11, "Down", 1, "Get off"),

    # Passenger(49, -15, -5, "Down", 1, "Get off"),
    # Passenger(50, -15, -6, "Down", 2, "Get off"),
    # Passenger(51, -15, -7, "Down", 3, "Get off"),
    # Passenger(52, -15, -8, "Down", 1, "Get off"),
    # Passenger(53, -15, -9, "Down", 2, "Get off"),
    # Passenger(54, -15, -10, "Down", 3, "Get off"),
    # Passenger(55, -15, -11, "Down", 1, "Get off"),


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

# G1~G5:乗客数の降車駅に対するストレス度合を格納
G1 = [0]
G2 = [0]
G3 = [0]
G4 = [0]
G5 = [0]


def drawPassenger(person: Passenger, cv: canvas):
    try:
        cv.delete(f"P{person.id}")
        if -12 <= person.y <= 12:
            cv.create_oval(5+20*convertX(person.x), 5+20*convertY(person.y), 5+20*convertX(person.x+1),
                           5+20*convertY(person.y+1), fill="green", tag=f"P{person.id}")
    except Exception:  # as identifier:
        pass


def set_stressList():
    global G1, G2, G3, G4, G5,NX
    # 初期化
    G1 = []
    G2 = []
    G3 = []
    G4 = []
    G5 = []
    for p in agents:
        if p._GET_OFF_STATION == 1:
            if len(G1)<len(NX):
                G1.append(p.stress)
        elif p._GET_OFF_STATION == 2:
            G2.append(p.stress)
        elif p._GET_OFF_STATION == 3:
            G3.append(p.stress)
        elif p._GET_OFF_STATION == 4:
            G4.append(p.stress)
        elif p._GET_OFF_STATION == 5:
            G5.append(p.stress)

    for i in range(len(G1),len(NX)+1):
        G1.append(0)
    for i in range(len(G2),len(NX)+1):
        G2.append(0)
    for i in range(len(G3),len(NX)+1):
        G3.append(0)
    for i in range(len(G4),len(NX)+1):
        G4.append(0)
    for i in range(len(G5),len(NX)+1):
        G5.append(0)


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
    global t_m
    t_m -= 1
    move(agents, canvas)
    print(t_m)
    if t_m == 0:
        if train[0] == "Stop":
            turn(agents)
            global X
            X += 1
            set_stressList()
            show_graph()
        t_m = TURN_MOVING
        print(train)
    # drawPassenger(a, canvas)
    #tk.after(100, main)


create_seat(canvas)
create_cells(canvas)

while True:
    main()
    time.sleep(0.05)
    try:
        tk.update()
    except Exception as identifier:
        exit(0)


tk.mainloop()
