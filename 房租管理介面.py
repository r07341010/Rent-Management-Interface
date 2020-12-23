#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import math
import tkinter.font as tkFont
import pandas as pd

calculate_file_path = 'C:\\Users\\johnc\\Desktop\\房租計算表.csv'

df = pd.read_csv(calculate_file_path, encoding='utf-8')

window = tk.Tk()
fontStyle1 = tkFont.Font(size=10, family='微軟正黑體')
fontStyle2 = tkFont.Font(size=12, family='微軟正黑體')
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
    room_payday = list(df.固定繳費日)
    room_phone = list(df.聯絡電話)
    room_name = list(df.姓名)
    room_id = list(df.身分證字號)
    room_rent[change_room_index] = float(rent_entry.get())
    room_parking[change_room_index] = float(parking_entry.get())
    room_add[change_room_index] = float(add_person_entry.get())
    room_payday[change_room_index] = int(payday_entry.get())
    room_phone[change_room_index] = str(phone_entry.get())
    room_name[change_room_index] = str(name_entry.get())
    room_id[change_room_index] = str(id_entry.get())
    
    df = pd.DataFrame(list(zip(room, room_rent, room_parking, room_add, room_payday, room_phone, room_name, room_id)),
                               columns =['房別', '使用租金', '停車費用', '加人費用', '固定繳費日', '聯絡電話', '姓名', '身分證字號'])
    df.to_csv(calculate_file_path, encoding='utf-8-sig')
    df = pd.csv(calculate_file_path)

def ChangeInf():
    global room_change
    global change
    global rent_entry
    global parking_entry
    global add_person_entry
    global payday_entry
    global phone_entry
    global name_entry
    global id_entry
    window2 = tk.Toplevel(window)
    window2.title('更改房客資訊')
    window2.geometry('600x400')
    window2.configure(background='white')
    '''更改資料'''
    header_label = tk.Label(window2, text='更改房客資訊', bg="white", fg="grey", font=fontStyle2)
    header_label.grid(column=1, row=1, ipadx=5, pady=5, sticky='W')

    room_change = tk.Label(window2, text='選擇房號(這行要刪掉)',bg="white", fg="black", font=fontStyle1)
    room_change.grid(column=1, row=2, ipadx=5, pady=5)
    change = ttk.Label(window2, text="請選擇", font=fontStyle1)
    change.grid(column=4, row=2)
    room_change = tk.Label(window2, text='下拉選項',bg="white", fg="black", font=fontStyle1)
    room_change = ttk.Combobox(window2, width=17)
    room_change['value'] = room_list
    room_change.grid(column=2, row=2, ipadx=5, pady=5)
    # 選完確定按鈕
    action_change = ttk.Button(window2, text="確認", width=5, command=ChangeRoomInformation)
    action_change.grid(column=3, row=2, ipadx=5, pady=5)

    # 更改房租
    rent_label = tk.Label(window2, text='房租',bg="white", fg="black", font=fontStyle1)
    rent_label.grid(column=1, row=3, ipadx=5, pady=5)
    rent_frame = tk.Frame(window2)
    rent_entry = tk.Entry(window2, width=20)
    rent_entry.grid(column=2, row=3, ipadx=5, pady=5)

    # 更改停車費用
    parking_label = tk.Label(window2, text='停車費用',bg="white", fg="black", font=fontStyle1)
    parking_label.grid(column=1, row=4, ipadx=5, pady=5)
    parking_frame = tk.Frame(window2)
    parking_entry = tk.Entry(window2, width=20)
    parking_entry.grid(column=2, row=4, ipadx=5, pady=5)

    # 更改加人費用
    add_person_label = tk.Label(window2, text='加人費用',bg="white", fg="black", font=fontStyle1)
    add_person_label.grid(column=1, row=5, ipadx=5, pady=5)
    add_person_frame = tk.Frame(window2)
    add_person_entry = tk.Entry(window2, width=20)
    add_person_entry.grid(column=2, row=5, ipadx=5, pady=5)

    # 更改固定繳費日
    payday_label = tk.Label(window2, text='固定繳費日',bg="white", fg="black", font=fontStyle1)
    payday_label.grid(column=1, row=6, ipadx=5, pady=5)
    payday_frame = tk.Frame(window2)
    payday_entry = tk.Entry(window2, width=20)
    payday_entry.grid(column=2, row=6, ipadx=5, pady=5)

    # 更改連絡電話
    phone_label = tk.Label(window2, text='聯絡電話',bg="white", fg="black", font=fontStyle1)
    phone_label.grid(column=1, row=7, ipadx=5, pady=5)
    phone_frame = tk.Frame(window2)
    phone_entry = tk.Entry(window2, width=20)
    phone_entry.grid(column=2, row=7, ipadx=5, pady=5)

    # 更改姓名
    name_label = tk.Label(window2, text='姓名',bg="white", fg="black", font=fontStyle1)
    name_label.grid(column=1, row=8, ipadx=5, pady=5)
    name_frame = tk.Frame(window2)
    name_entry = tk.Entry(window2, width=20)
    name_entry.grid(column=2, row=8, ipadx=5, pady=5)

    # 更改身分證字號
    id_label = tk.Label(window2, text='身分證字號',bg="white", fg="black", font=fontStyle1)
    id_label.grid(column=1, row=9, ipadx=5, pady=5)
    id_frame = tk.Frame(window2)
    id_entry = tk.Entry(window2, width=20)
    id_entry.grid(column=2, row=9, ipadx=5, pady=5)

    # 確定更改按鈕
    change_btn = tk.Button(window2, text='確定更改', command=ChangeRent, bg="white", fg="black", font=fontStyle1)
    change_btn.grid(column=3, row=9, ipadx=5, pady=5, columnspan=2, sticky='W')

    window2.mainloop()

other = ''
rent, other_charge=0,0
list_53 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
room_list = tuple(df.房別)
change_room_index = ''
change_rent = 0
change_parking = 0
change_add_person = 0
change_payday = 0
change_phone = ''
change_name = ''
change_id = ''

'''房客資料'''
title_label = tk.Label(window, text='53-101房客資料', bg="white", fg="grey", font=fontStyle2)
title_label.grid(column=1, row=3, ipadx=5, pady=5, sticky='W', columnspan=2)

roomindex = 0  # 之後改成前一個介面選的房號
# 姓名
title1_label = tk.Label(window, text='姓名：', bg="white", fg="black", font=fontStyle1)
title1_label.grid(column=1, row=4, ipadx=5, pady=5)
inf1_label = tk.Label(window, text=list(df.姓名)[roomindex], bg="white", fg="black", font=fontStyle1)
inf1_label.grid(column=2, row=4, ipadx=5, pady=5, sticky='W')

# 聯絡電話
title2_label = tk.Label(window, text='聯絡電話：', bg="white", fg="black", font=fontStyle1)
title2_label.grid(column=1, row=5, ipadx=5, pady=5)
inf2_label = tk.Label(window, text='0' + str(list(df.聯絡電話)[roomindex]), bg="white", fg="black", font=fontStyle1)
inf2_label.grid(column=2, row=5, ipadx=5, pady=5, sticky='W')

# 身分證字號
title3_label = tk.Label(window, text='身分證字號：', bg="white", fg="black", font=fontStyle1)
title3_label.grid(column=1, row=6, ipadx=5, pady=5)
inf3_label = tk.Label(window, text=list(df.身分證字號)[roomindex].strip(), bg="white", fg="black", font=fontStyle1)
inf3_label.grid(column=2, row=6, ipadx=5, pady=5, sticky='W')

# 固定繳費日
title4_label = tk.Label(window, text='固定繳費日：', bg="white", fg="black", font=fontStyle1)
title4_label.grid(column=1, row=7, ipadx=5, pady=5)
inf4_label = tk.Label(window, text=str(list(df.固定繳費日)[roomindex]) + '日', bg="white", fg="black", font=fontStyle1)
inf4_label.grid(column=2, row=7, ipadx=5, pady=5, sticky='W')

# 使用租金
title5_label = tk.Label(window, text='使用租金：', bg="white", fg="black", font=fontStyle1)
title5_label.grid(column=1, row=8, ipadx=5, pady=5)
inf5_label = tk.Label(window, text=str(list(df.使用租金)[roomindex]) + '元', bg="white", fg="black", font=fontStyle1)
inf5_label.grid(column=2, row=8, ipadx=5, pady=5, sticky='W')

# 停車費用
title6_label = tk.Label(window, text='停車費用：', bg="white", fg="black", font=fontStyle1)
title6_label.grid(column=1, row=9, ipadx=5, pady=5)
inf6_label = tk.Label(window, text=str(list(df.停車費用)[roomindex]) + '元', bg="white", fg="black", font=fontStyle1)
inf6_label.grid(column=2, row=9, ipadx=5, pady=5, sticky='W')

# 加人費用
title7_label = tk.Label(window, text='加人費用：', bg="white", fg="black", font=fontStyle1)
title7_label.grid(column=1, row=10, ipadx=5, pady=5)
inf8_label = tk.Label(window, text=str(list(df.加人費用)[roomindex]) + '元', bg="white", fg="black", font=fontStyle1)
inf8_label.grid(column=2, row=10, ipadx=5, pady=5, sticky='W')

# 更改資料
changebtt1 = ttk.Button(window, text="更改資料", command=ChangeInf)
changebtt1.grid(column=1, row=11, ipadx=5, pady=5)

'''計算房租介面'''
# 介面名稱
header_label = tk.Label(window, text='計算房租介面', bg="white", fg="grey", font=fontStyle2)
header_label.grid(column=1, row=12, ipadx=5, pady=5, sticky='W')

# 第二列為選擇房號
# # room_frame = tk.Frame(window)
room_label = tk.Label(window, text='選擇房號(這行要刪掉)',bg="white", fg="black", font=fontStyle1)
room_label.grid(column=1, row=13, ipadx=5, pady=5)
label1 = ttk.Label(window, text="請選擇", font=fontStyle1)
label1.grid(column=3, row=13, sticky='E')
room_label = tk.Label(window, text='下拉選項',bg="white", fg="black", font=fontStyle1)
room_label = ttk.Combobox(window, width=17)
room_label['value'] = room_list
room_label.grid(column=2, row=13, ipadx=5, pady=5)
# 選完確定按鈕
action = ttk.Button(window, text="確認", width=3, command=ClickMe)
action.grid(column=3, row=13, ipadx=5, pady=5, sticky='W')

# 第三列為時間
time_label = tk.Label(window, text='時間',bg="white", fg="black", font=fontStyle1)
time_label.grid(column=1, row=14, ipadx=5, pady=5)
time_frame = tk.Frame(window)
time_entry = tk.Entry(window, width=20)
time_entry.grid(column=2, row=14, ipadx=5, pady=5)

# 第四列為前一月份電錶度數
previous_label = tk.Label(window, text='前月電錶顯示（度）',bg="white", fg="black", font=fontStyle1)
previous_label.grid(column=1, row=15, ipadx=5, pady=5)
previous_frame = tk.Frame(window)
previous_entry = tk.Entry(window, width=20)
previous_entry.grid(column=2, row=15, ipadx=5, pady=5)

# 第五列為本月份電錶度數
month_label = tk.Label(window, text='本月電錶顯示（度）',bg="white", fg="black", font=fontStyle1)
month_label.grid(column=1, row=16, ipadx=5, pady=5)
month_frame = tk.Frame(window)
month_entry = tk.Entry(window, width=20)
month_entry.grid(column=2, row=16, ipadx=5, pady=5)

# 第六列為計算按鈕
calculate_btn = tk.Button(window, text='計算本月房租', command=CalculateRent, fg="black", font=fontStyle1)
calculate_btn.grid(column=3, row=16, ipadx=5, pady=5)

# 第七列為結果顯示窗格
result_label = tk.Label(window, font=fontStyle1)
result_label.grid(column=1, row=17, ipadx=5, pady=5, rowspan=5, columnspan=6, sticky='W')

window.mainloop()
