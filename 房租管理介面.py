#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import math
import tkinter.font as tkFont
import pandas as pd

calculate_file_path = '/Users/apple/Desktop/房租計算表.csv'

df = pd.read_csv(calculate_file_path)

window = tk.Tk()
fontStyle = tkFont.Font(size=20)
window.title('房租管理介面')
window.geometry('800x600')
window.configure(background='white')

def CalculateRent():
    global other_charge
    global rent
    global other
    time = time_entry.get()
    previous = float(previous_entry.get())
    month = float(month_entry.get())
    power = round(month - previous, 2)
    if len(other) > 0: # 有其他費用：停車費或加人費用
        # calculate the ouput content
        pay = rent + power*5 + other_charge
        head = '親愛的' + room_list[room_label.current()] + '房客您好，本期({:>})的房租費用'.format(time)
        total = '總計{:<8}元，其中包含：\n'.format(format(pay,',')) # 千分位處理
        rent_show = '1.租金{:<8}元\n'.format(format(rent,',')) # 千分位處理
        power = '2.電費：本月耗電 {:<.1f} 度，小計 {:<.1f} 元。(上個月為 {:<.1f} 度電，本月為{:<.1f} 度電。)\n'.format(power,power*5,previous,month)
        # print the output
        result = head + total + rent_show + power + other
        print('有其他費用 = ',other)
    else: # 無其他費用：停車費或加人費用
        # calculate the ouput content
        pay = rent + power*5
        head = '親愛的' + room_list[room_label.current()] + '房客您好，本期({:>})的房租費用'.format(time)
        total = '總計{:<8}元，其中包含：\n'.format(format(pay,',')) # 千分位處理
        rent_show = '1.租金{:<8}元\n'.format(format(rent,',')) # 千分位處理
        power = '2.電費：本月耗電 {:<.1f} 度，小計 {:<.1f} 元。(上個月為 {:<.1f} 度電，本月為{:<.1f} 度電。)\n'.format(power,power*5,previous,month)
        # print the output
        result = head + total + rent_show + power
        print('無其他費用 = ',other)
    if room_label.current() in list_53 :# 如果是53號公寓
        warning = '*** 小叮嚀：夜歸辛苦靜悄悄，垃圾分類請做好。 ***'
        result = result + warning
    else:
        pass
    
    # 介面顯示結果
    result_label.configure(text=result)
    # automatically copy the output
    r = tk.Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(result)
    r.destroy()
    
def ClickMe():
    print(room_label.current())
    global other_charge
    global rent
    global other
    index = room_label.current()
    df = pd.read_csv(calculate_file_path)
    # 顯示房別
    label1.config(text=df.房別[index])
    # 顯示租金與其他費用
    parking = df.停車費用[index]
    print('parking',parking)
    add_person = df.加人費用[index]
    print('add_person',add_person)
    rent, other_charge = df.使用租金[index], parking + add_person
    print('other_charge',other_charge)
    other = ''
    # 衡量是否需要顯示其他費用
    if parking + add_person == 0 :
        print('parking + add_person == 0 ')
        pass
    elif parking > 0 and add_person == 0 :
        print('parking > 0 and add_person == 0')
        other = '3. 停車費用為'+str(parking)+'元。\n'
    elif parking == 0 and add_person > 0 :
        print('parking == 0 and add_person > 0 ')
        other = '3. 加人費用為'+str(add_person)+'元。\n'
    elif parking > 0 and add_person > 0 :
        print('parking > 0 and add_person > 0 ')
        other = '3. 停車費用為'+str(parking)+'元，以及加人費用為'+str(add_person)+'元。\n'
    return

def ChangeRoomInformation():
    global change_room_index
    change_room_index = room_change.current()
    # 顯示房別
    change.config(text=df.房別[change_room_index])
def ChangeRent():
    global change_room_index
    global change_rent
    global change_parking
    global change_add_person
    global df
    room = list(df.房別)
    room_rent = list(df.使用租金)
    room_parking = list(df.停車費用)
    room_add = list(df.加人費用)
    room_rent[change_room_index] = float(rent_entry.get())
    room_parking[change_room_index] = float(parking_entry.get())
    room_add[change_room_index] = float(add_person_entry.get())
    df = pd.DataFrame(list(zip(room, room_rent, room_parking, room_add)), columns =['房別', '使用租金', '停車費用', '加人費用'])
    df.to_csv(calculate_file_path)
    df = pd.csv(calculate_file_path)

other = ''
rent, other_charge=0,0
list_53 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
room_list = tuple(df.房別)
change_room_index = ''
change_rent = 0
change_parking = 0
change_add_person = 0

### 計算房租介面 ###
# 介面名稱
header_label = tk.Label(window, text='計算房租介面',bg="white", fg="gray", font=fontStyle)
header_label.grid(column=1, row=3, ipadx=15, pady=10)

# 第二列為時間
time_label = tk.Label(window, text='時間',bg="white", fg="black", font=fontStyle)
time_label.grid(column=2, row=3, ipadx=15, pady=10)
time_frame = tk.Frame(window)
time_entry = tk.Entry(window, width=20)
time_entry.grid(column=3, row=3, ipadx=15, pady=10)

# 第三列為選擇房號
# # room_frame = tk.Frame(window)
room_label = tk.Label(window, text='選擇房號',bg="white", fg="black", font=fontStyle)
room_label.grid(column=2, row=8, ipadx=15, pady=10)
label1 = ttk.Label(window, text="請選擇", font=fontStyle)
label1.grid(column=6, row=8)
room_label = tk.Label(window, text='下拉選項',bg="white", fg="black", font=fontStyle)
room_label = ttk.Combobox(window)
room_label['value'] = room_list
room_label.grid(column=3, row=8, ipadx=15, pady=10)
# 選完確定按鈕
action = ttk.Button(window, text="確認", command=ClickMe)
action.grid(column=5, row=8, ipadx=15, pady=10)

# 第四列為前一月份電錶度數
previous_label = tk.Label(window, text='前月電錶顯示（度）',bg="white", fg="black", font=fontStyle)
previous_label.grid(column=2, row=13, ipadx=15, pady=10)
previous_frame = tk.Frame(window)
previous_entry = tk.Entry(window, width=20)
previous_entry.grid(column=3, row=13, ipadx=15, pady=10)

# 第五列為本月份電錶度數
month_label = tk.Label(window, text='本月電錶顯示（度）',bg="white", fg="black", font=fontStyle)
month_label.grid(column=2, row=18, ipadx=15, pady=10)
month_frame = tk.Frame(window)
month_entry = tk.Entry(window, width=20)
month_entry.grid(column=3, row=18, ipadx=15, pady=10)

# 第六列為計算按鈕
calculate_btn = tk.Button(window, text='計算本月房租', command=CalculateRent,bg="white", fg="black", font=fontStyle)
calculate_btn.grid(column=2, row=23, ipadx=15, pady=10)

# 第七列為結果顯示窗格
result_label = tk.Label(window, font=fontStyle)
result_label.grid(column=2, row=28, ipadx=15, pady=10,rowspan=5,columnspan=5)

# 介面名稱
header_label = tk.Label(window, text='更改房租資料',bg="white", fg="gray", font=fontStyle)
header_label.grid(column=1, row=33, ipadx=15, pady=10)

### 更改房務資料 ###
room_change = tk.Label(window, text='選擇房號',bg="white", fg="black", font=fontStyle)
room_change.grid(column=2, row=33, ipadx=15, pady=10)
change = ttk.Label(window, text="請選擇", font=fontStyle)
change.grid(column=6, row=33)
room_change = tk.Label(window, text='下拉選項',bg="white", fg="black", font=fontStyle)
room_change = ttk.Combobox(window)
room_change['value'] = room_list
room_change.grid(column=3, row=33, ipadx=15, pady=10)
# 選完確定按鈕
action_change = ttk.Button(window, text="確認", command=ChangeRoomInformation)
action_change.grid(column=5, row=33, ipadx=15, pady=10)

# 第四列為前一月份電錶度數
rent_label = tk.Label(window, text='房租',bg="white", fg="black", font=fontStyle)
rent_label.grid(column=2, row=38, ipadx=15, pady=10)
rent_frame = tk.Frame(window)
rent_entry = tk.Entry(window, width=20)
rent_entry.grid(column=3, row=38, ipadx=15, pady=10)

# 第五列為本月份電錶度數
parking_label = tk.Label(window, text='停車費用',bg="white", fg="black", font=fontStyle)
parking_label.grid(column=2, row=43, ipadx=15, pady=10)
parking_frame = tk.Frame(window)
parking_entry = tk.Entry(window, width=20)
parking_entry.grid(column=3, row=43, ipadx=15, pady=10)

add_person_label = tk.Label(window, text='加人費用',bg="white", fg="black", font=fontStyle)
add_person_label.grid(column=2, row=48, ipadx=15, pady=10)
add_person_frame = tk.Frame(window)
add_person_entry = tk.Entry(window, width=20)
add_person_entry.grid(column=3, row=48, ipadx=15, pady=10)

# 第六列為計算按鈕
change_btn = tk.Button(window, text='確定更改', command=ChangeRent,bg="white", fg="black", font=fontStyle)
change_btn.grid(column=2, row=53, ipadx=15, pady=10)

window.mainloop()
