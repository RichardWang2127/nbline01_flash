import threading
import time
from tkinter import *
import os
from tkinter.messagebox import *

# import webbrowser
# import sys
# from pygame.locals import *
# import pygame
"""Code by 宁波轨道交通1号线(Bilibili) & Design by Ningbo Rail Transit(Official)"""

current_pos = os.getcwd()  # 获取本文件的路径
print(f"Position: \"{current_pos}\"")

version = "1.0"

"""窗口"""
win = Tk()

"""变量初始化"""
started = False
rate = 1.0
direction = "right"
door = "current"
train_dir = "right"
visited = 0
train_status = "stop"
total_sta = 29
is_single_scr = True

over_title = "宁波轨道交通1号线闪灯图模拟"

win.title(over_title)
win.resizable(False, False)

w = (win.winfo_screenwidth() - 370 - 100)
h = (win.winfo_screenheight() - 370 - 100)

win.geometry(f"{370}x{370}+{w}+{h - 10}")

mf = "宋体"  # main font
mf_eng = "Times New Roman"

stations = ["高桥西|Gaoqiao West", "高桥|Gaoqiao", "梁祝|Liangzhu", "芦港|Lugang", "徐家漕长乐|Xujiacao Changle",
            "望春桥|Wangchun Bridge", "泽民|Zemin", "大卿桥|Daqing Bridge", "西门口|Ximenkou", "鼓楼|Gulou",
            "东门口(天一广场)|Dongmenkou(Tianyi Square)", "江厦桥东|Jiangxia Bridge East",
            "舟孟北路|Zhoumeng North Road",
            "樱花公园|Sakura Park", "福明路|Fuming Road", "世纪大道|Shiji Ave", "海晏北路|Haiyan North Road",
            "福庆北路|Fuqing North Road",
            "盛莫路|Shengmo Road", "东环南路|Donghuan South Road", "邱隘东|Qiuga East", "五乡|Wuxiang",
            "宝幢|Baozhuang", "邬隘|Wuga",
            "大碶|Daqi", "松花江路|Songhuajiang Road", "中河路|Zhonghe Road", "长江路|Changjiang Road", "霞浦|Xiapu"]

stations_rev = []

for i in range(0, len(stations)):
    stations_rev.append(stations[len(stations) - i - 1])

print(f"{len(stations)} {len(stations_rev)} {len(stations) == len(stations_rev)}")
print(stations)
print(stations_rev)

terminals_1 = ["高桥西"]  # "望春桥"

terminals_2 = ["霞浦"]  # "宝幢", "东环南路"

transfer_list = ["#D51519", "#F09812", "#ABCC13", "#202084"]

control_btn_disp = ["发车", "停车"]

control_id = 0

"""调试用-返回点击时的坐标"""


def prt(event):
    print(event.x, end=", ")
    print(event.y)


"""显示"""


def flash():
    while control_id == 1:
        if quit_needed:
            return 0
        cav.create_oval(x_pt_1, start_pt_y, x_pt_1 + size, start_pt_y + size, fill="#FFCD0A", outline="black", width=3)
        if door == "current":
            cav.create_oval(1770, 120, 1810, 160, fill="#00FF8C", outline="black", width=3)
        else:
            cav.create_oval(1770, 190, 1810, 230, fill="red", outline="black", width=3)
        time.sleep(0.15)
        if quit_needed:
            return 0
        cav.create_oval(x_pt_1, start_pt_y, x_pt_1 + size, start_pt_y + size, fill="white", outline="black", width=3)
        if door == "current":
            cav.create_oval(1770, 120, 1810, 160, fill="white", outline="black", width=3)
        else:
            cav.create_oval(1770, 190, 1810, 230, fill="white", outline="black", width=3)
        time.sleep(0.15)
    return 0


def control():
    global control_id, x_pt_1, control_btn, light_flash, quit_needed, visited
    if visited == 29:
        return 19

    if control_id == 0:
        control_btn.place_forget()
        control_id = 1
        control_btn = Button(win, text=control_btn_disp[control_id], font=(mf, 13), command=control)
        control_btn.place(x=180, y=280, anchor=CENTER)

        if train_dir == "right":
            for ff in range(0, visited):
                x_pt_2 = start_pt_x + ff * (size + dist)
                cav.create_oval(x_pt_2, start_pt_y, x_pt_2 + size, start_pt_y + size, fill="red", outline="black",
                                width=3)
            x_pt_1 = start_pt_x + visited * (size + dist)

        else:
            for ff in range(total_sta - 1, total_sta - visited - 2, -1):
                x_pt_2 = start_pt_x + ff * (size + dist)
                cav.create_oval(x_pt_2, start_pt_y, x_pt_2 + size, start_pt_y + size, fill="red", outline="black",
                                width=3)
            x_pt_1 = start_pt_x + (total_sta - visited - 1) * (size + dist)

        light_flash = threading.Thread(target=flash)
        quit_needed = False
        light_flash.start()
    elif control_id == 1:
        control_btn.place_forget()
        control_id = 0
        quit_needed = True
        control_btn = Button(win, text=control_btn_disp[control_id], font=(mf, 13), command=control)
        control_btn.place(x=180, y=280, anchor=CENTER)
        # time.sleep(0.32)
        if train_dir == "right":
            for ff in range(0, visited + 1):
                x_pt_2 = start_pt_x + ff * (size + dist)
                cav.create_oval(x_pt_2, start_pt_y, x_pt_2 + size, start_pt_y + size, fill="red", outline="black",
                                width=3)
            visited += 1

        else:
            for ff in range(total_sta - visited - 1, total_sta):
                print(ff, end=", ")
                x_pt_2 = start_pt_x + ff * (size + dist)
                print(x_pt_2, end=";")
                cav.create_oval(x_pt_2, start_pt_y, x_pt_2 + size, start_pt_y + size, fill="red", outline="black",
                                width=3)
            visited += 1
            print()
        if door == "current":
            cav.create_oval(1770, 120, 1810, 160, fill="#00FF8C", outline="black", width=3)
        else:
            cav.create_oval(1770, 190, 1810, 230, fill="red", outline="black", width=3)
        # for ff in range(0, visited + 1):
        #     x_pt_2 = start_pt_x + ff * (size + dist)
        #     cav.create_oval(x_pt_2, start_pt_y, x_pt_2 + size, start_pt_y + size, fill="red", outline="black",
        #     width=3)
        # visited += 1
    return 1145142333


def display2():  # drawing
    global start_pt_x, start_pt_y, size, dist
    cav.create_oval(5 * rate, 30 * rate, 45 * rate, 70 * rate, fill="#1B88B8", outline="black", width=2)
    cav.create_oval(150 * rate, 30 * rate, 190 * rate, 70 * rate, fill="#1B88B8", outline="black", width=2)
    cav.create_text(99 * rate, 50 * rate, text="列车运行方向", anchor=CENTER, font=("黑体", int(12 * rate)))
    cav.create_text(99 * rate, 80 * rate, text="Train Running Direction", anchor=CENTER, font=("Segoe UI", 10))
    cav.bind("<ButtonPress-1>", prt)
    standard_pt_v = 50
    standard_pt_value_y = 50

    colors_l = ["white", "#00FF8C"]
    "左箭头"
    cav.create_line(15 * rate, standard_pt_v * rate, 40 * rate, standard_pt_v * rate,
                    fill=colors_l[train_dir == "left"], width=5)
    """上方"""
    point1 = (17 * rate, standard_pt_value_y * rate)
    point2 = (27 * rate, (standard_pt_value_y - 9.5) * rate)
    point3 = (20 * rate, (standard_pt_value_y - 9.5) * rate)
    point4 = (10 * rate, standard_pt_value_y * rate)
    cav.create_polygon(*point1, *point2, *point3, *point4, fill=colors_l[train_dir == "left"])

    "下方"
    point5 = (18 * rate, standard_pt_value_y * rate)
    point6 = (28 * rate, (standard_pt_value_y + 9.5) * rate)
    point7 = (21 * rate, (standard_pt_value_y + 9.5) * rate)
    point8 = (11 * rate, standard_pt_value_y * rate)
    cav.create_polygon(*point5, *point6, *point7, *point8, fill=colors_l[train_dir == "left"])

    "右箭头"
    cav.create_line(155 * rate, standard_pt_v * rate, 180 * rate, standard_pt_v * rate,
                    fill=colors_l[train_dir == "right"], width=5)
    """上方"""
    point1 = (188 * rate, standard_pt_value_y * rate)
    point2 = (178 * rate, (standard_pt_value_y - 9.5) * rate)
    point3 = (171 * rate, (standard_pt_value_y - 9.5) * rate)
    point4 = (181 * rate, standard_pt_value_y * rate)
    cav.create_polygon(*point1, *point2, *point3, *point4, fill=colors_l[train_dir == "right"])

    "下方"
    point5 = (188 * rate, standard_pt_value_y * rate)
    point6 = (178 * rate, (standard_pt_value_y + 9.5) * rate)
    point7 = (171 * rate, (standard_pt_value_y + 9.5) * rate)
    point8 = (181 * rate, standard_pt_value_y * rate)
    cav.create_polygon(*point5, *point6, *point7, *point8, fill=colors_l[train_dir == "right"])

    cav.create_text(99 * rate, 150 * rate, anchor=CENTER, text="轨道交通1号线运营图", font=("黑体", int(12 * rate)))
    cav.create_text(99 * rate, 180 * rate, anchor=CENTER, text="Rail Transit Line 1 Network Map",
                    font=("Segoe UI", int(10 * rate)))

    if train_dir == "left":
        left_sta = end_sta
        right_sta = start_sta
    else:
        left_sta = start_sta
        right_sta = end_sta
    print(left_sta + right_sta)

    needed = stations
    print(left_sta)
    if left_sta == "霞浦" or left_sta == "东环南路":
        print(True)
        needed = stations_rev

    start_pt_x = 200 * rate
    start_pt_y = 230 * rate
    size = 25 * rate
    dist = 25 * rate

    for f in range(0, 29):
        x_pt = start_pt_x + f * (size + dist)
        # if f != -1:
        cav.create_text(x_pt + 0, start_pt_y - 10, text=needed[f].replace("|", " "),
                        angle=40, font=("微软雅黑", int(12 * rate)), anchor=W)
        if f != 28:
            cav.create_rectangle(x_pt + size / 2, start_pt_y + 5, x_pt + size + dist + size / 2, start_pt_y + size - 5,
                                 fill="#1B88B8", width=0)
            # print(f"{x_pt + size / 2} {start_pt_y} {x_pt + size / 2} {start_pt_y + size}")

        """绘制换乘信息"""
        clr = "white"
        if needed[f] == "海晏北路|Haiyan North Road":
            clr = transfer_list[3]
        elif needed[f] == "樱花公园|Sakura Park":
            clr = transfer_list[1]
        elif needed[f] == "鼓楼|Gulou":
            clr = transfer_list[0]
        elif needed[f] == "大卿桥|Daqing Bridge":
            clr = transfer_list[2]
        for k in range(0, 4):
            if transfer_list[k] == needed[f]:
                clr = transfer_list[k][transfer_list[k].find("|") + 1: -1]
                print(clr)
        point09 = (x_pt, start_pt_y + size / 2)
        point10 = (x_pt, start_pt_y + size + 15 * rate)
        point11 = (x_pt + size / 2, start_pt_y + size + 30 * rate)
        point12 = (x_pt + size, start_pt_y + size + 15 * rate)
        point13 = (x_pt + size, start_pt_y + size / 2)
        cav.create_polygon(*point09, *point10, *point11, *point12, *point13, fill=clr, width=0)
        try:
            cav.create_text(x_pt + size / 2, 290 * rate, text=f"换乘{transfer_list.index(clr) + 2}号线",
                            font=("微软雅黑", int(11 * rate)), anchor=CENTER)
        except ValueError:
            pass

        try:
            cav.create_text(x_pt + size / 2, (290 + 15) * rate,
                            text=f"Transfer to Line {transfer_list.index(clr) + 2}", font=("微软雅黑", int(8 * rate)),
                            anchor=CENTER)
        except ValueError:
            pass

        cav.create_oval(x_pt, start_pt_y, x_pt + size, start_pt_y + size, fill="white", outline="black", width=3)

    """显示绿灯"""
    """前往高桥西"""
    if left_sta == "高桥西" or right_sta == "高桥西":
        start_pt_x = 200 * rate

        for f in range(0, 20):
            x_pt = start_pt_x + f * (size + dist)
            cav.create_oval(x_pt, start_pt_y, x_pt + size, start_pt_y + size, fill="#00FF8C", outline="black", width=3)

    """前往望春桥"""
    if left_sta == "望春桥" or right_sta == "望春桥":
        start_pt_x = 200 * rate

        for f in range(5, 20):
            x_pt = start_pt_x + f * (size + dist)
            cav.create_oval(x_pt, start_pt_y, x_pt + size, start_pt_y + size, fill="#00FF8C", outline="black", width=3)

    """前往东环南路(无需任何操作)"""
    if left_sta == "东环南路" or right_sta == "东环南路":
        pass

    """前往霞浦"""
    if left_sta == "霞浦" or right_sta == "霞浦":
        start_pt_x = 200 * rate

        for f in range(20, 29):
            x_pt = start_pt_x + f * (size + dist)
            cav.create_oval(x_pt, start_pt_y, x_pt + size, start_pt_y + size, fill="#00FF8C", outline="black", width=3)

    """开门方向区域"""
    cav.create_oval(1770, 120, 1810, 160, fill="white", outline="black", width=3)
    cav.create_oval(1770, 190, 1810, 230, fill="white", outline="black", width=3)
    cav.create_text(1890, 130, text="本侧开门", font=("微软雅黑", 18), anchor=CENTER)
    cav.create_text(1890, 165, text="Doors Open\nat This Side", font=("微软雅黑", 10), anchor=CENTER)
    cav.create_text(1890, 200, text="对侧开门", font=("微软雅黑", 18), anchor=CENTER)
    cav.create_text(1890, 235, text="Doors Open at\nThe Other Side", font=("微软雅黑", 10), anchor=CENTER)


def notice_btn_1():
    try:
        notice02.pack_forget()
        notice03.pack_forget()
    except NameError:
        pass
    notice01.pack(anchor=CENTER)

    return 0


def notice_btn_2():
    try:
        notice01.pack_forget()
        notice03.pack_forget()
    except NameError:
        pass
    notice02.pack(anchor=CENTER)

    return 0


def notice_btn_3():
    try:
        notice01.pack_forget()
        notice02.pack_forget()
    except NameError:
        pass
    notice03.pack(anchor=CENTER)

    return 0


def display_win_des():
    global started, control_id, visited, quit_needed
    started = False
    visited = 0
    quit_needed = True
    display_win.destroy()
    control_btn.place_forget()
    control_id = 0


def start_display():
    global started, start_sta, end_sta, visited, quit_needed, control_id
    if started:
        return 114514
    started = True
    start_sta = end_sta = ""
    if direction == "right":
        start_sta = v.get()
        end_sta = v2.get()
    else:
        start_sta = v2.get()
        end_sta = v.get()
    print(start_sta + end_sta + direction + door + train_dir)
    """显示窗口"""
    global cav, display_win, rate
    display_win = Tk()
    sz = win.winfo_screenwidth() - 50
    w2 = 15
    h2 = 50
    # rate = 0.7
    display_win.geometry(f"{sz}x{int(380 * rate)}+{w2}+{h2}")
    quit_needed = False
    display_win.title("显示区")
    # notice_no_large = Label(display_win, text="请不要缩放本页面!", fg="red", font=("楷体", 25))
    # notice_no_large.place(x=1000, y=350, anchor=S)
    cav = Canvas(display_win, width=2100, height=330 * rate, bg="white")
    cav.pack()
    display_win.protocol("WM_DELETE_WINDOW", display_win_des)
    display2()
    control_id = 0
    control_btn.config(text=control_btn_disp[control_id])
    control_btn.place(x=180, y=280, anchor="center")
    display_win.mainloop()


def show_notice():
    global notice01, notice02, notice03
    notice_win = Tk()
    notice_win.title("公告")
    # notice_win.geometry("700x200")
    button01 = Button(notice_win, text="1", command=notice_btn_1)
    button02 = Button(notice_win, text="2", command=notice_btn_2)
    button03 = Button(notice_win, text="3", command=notice_btn_3)

    # notice00 = Label(notice_win, text="请点击左边的按钮")
    notice01 = Label(notice_win, font=("宋体", 12), text=("欢迎使用本应用!(喜)\n"
                                                          "本应用免费，作者B站：宁波轨道交通1号线。如有假冒、伪劣、抄袭、搬运、售卖的请联系我，感谢!\n"
                                                          "Code by 王Richard(B站宁波轨道交通1号线) & "
                                                          "Design by Ningbo Rail Transit(Official)"))
    notice02 = Label(notice_win, font=("宋体", 12),
                     text="须知\n本软件免费，请合理使用，严禁售卖。\n如有意见或反馈，可以点击配置界面左下角联系我，有想要的功能也可以。")
    notice03 = Label(notice_win, font=("宋体", 12), text=(
        f"版本须知\n版本号: {version}\n此版本内容: 宁波轨道交通1号线闪灯图基础内容(有不足)。\n"
        f"目前缺少内容: \n1. 小交路\n2. 多窗口显示\n3. 使用其他方式绘制(目前清晰度太低，是刚开始乱搓的)\n4. 不知道，你们提\n会按照标号顺序来加(1最先)。"))
    button01.pack()
    button02.pack()
    button03.pack()
    return 0


def train_left_right():
    global train_dir
    train_dir_left.place_forget()
    train_dir_right.place(x=235, y=134, anchor="center")
    train_dir = "right"
    return


def train_right_left():
    global train_dir
    train_dir_right.place_forget()
    train_dir_left.place(x=235, y=134, anchor="center")
    train_dir = "left"
    return


def left_btn_to_right():
    global direction
    left_btn.place_forget()
    right_btn.place(x=180, y=66, anchor="center")
    direction = "right"
    return


def right_btn_to_left():
    global direction
    right_btn.place_forget()
    left_btn.place(x=180, y=66, anchor="center")
    direction = "left"
    return


def cur_to_other():
    global door
    cur_door_btn.place_forget()
    other_door_btn.place(x=135, y=134, anchor="center")
    door = "other"
    return


def other_to_cur():
    global door
    other_door_btn.place_forget()
    cur_door_btn.place(x=135, y=134, anchor="center")
    door = "current"
    return


def single_to_multi():
    global is_single_scr
    single_screen_btn.place_forget()
    multi_screen_btn.place(x=180, y=170, anchor="center")
    is_single_scr = False
    return


def multi_to_single():
    global is_single_scr
    multi_screen_btn.place_forget()
    single_screen_btn.place(x=180, y=170, anchor="center")
    is_single_scr = True
    return


def win_destroy():
    showinfo("感谢", "感谢使用本软件!")
    win.destroy()
    quit()


def destroy_directly():
    win.destroy()
    quit(1910420)


def show_contact():
    showinfo("联系方式", "B站: 宁波轨道交通1号线, QQ: 250026470, 欢迎提交意见和反馈。")


win.protocol("WM_DELETE_WINDOW", win_destroy)
title_msg = Label(win, text="宁波轨道交通1号线闪灯图配置页面", font=(mf, 17))
title_msg.pack()

msg_control = Label(win, text="控制区", font=(mf, 17))

msg_control.place(x=180, y=200, anchor="center")

contact = Button(win, text="联系作者", command=show_contact, font=(mf, 13))
contact.place(x=0, y=370, anchor=SW)
notice = ""
btn_notice = "↑\n戳一下更改\n↓"
v = StringVar(win)
left_btn = Button(win, text="<-", font=(mf, 13), command=left_btn_to_right)
right_btn = Button(win, text="->", font=(mf, 13), command=right_btn_to_left)
cur_door_btn = Button(win, text="开本侧门", font=(mf, 13), command=cur_to_other)
other_door_btn = Button(win, text="开对侧门", font=(mf, 13), command=other_to_cur)
train_dir_right = Button(win, text="列车方向->", font=(mf, 13), command=train_right_left)
train_dir_left = Button(win, text="<-列车方向", font=(mf, 13), command=train_left_right)
control_btn = Button(win, text=control_btn_disp[control_id], font=(mf, 13), command=control)
show = Button(win, text="公告(首次使用请点击)", font=(mf, 13), command=show_notice)
start = Button(win, text="启动!", font=(mf, 13), command=start_display)
select = OptionMenu(win, v, *terminals_1)
show_notice = Label(win, text=btn_notice, font=(mf, 8))
single_screen_btn = Button(win, text="显示在一个窗口", command=single_to_multi, font=(mf, 13))
multi_screen_btn = Button(win, text="显示在多个窗口", command=multi_to_single, font=(mf, 13))
v.set(terminals_1[0])
v2 = StringVar(win)
select2 = OptionMenu(win, v2, *terminals_2)
v2.set(terminals_2[0])
right_btn.place(x=180, y=66, anchor="center")
select.place(x=40, y=50)
select2.place(x=240, y=50)
show_notice.place(x=180, y=101, anchor="center")
cur_door_btn.place(x=135, y=134, anchor="center")
train_dir_right.place(x=235, y=134, anchor="center")
start.place(x=180, y=240, anchor="center")
show.place(x=370, y=370, anchor=SE)
single_screen_btn.place(x=180, y=170, anchor="center")
terminal_soft = Button(win, text="结束任务", command=destroy_directly)
quit_soft = Button(win, text="退出", command=win_destroy)
terminal_soft.place(x=185, y=370, anchor=SE)
quit_soft.place(x=126, y=370, anchor=SE)

win.mainloop()
