import tkinter as tk
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import tkinter.font as tkFont
import pandas as pd
import datetime
#df = pd.read_csv(r'C:\Users\user\Documents\GitHub\Rent-Management-Interface\房租計算表.csv')
df = pd.read_csv(r'/Users/apple/Desktop/github_final/Rent-Management-Interface/房租計算表.csv')
window = tk.Tk()
fontStyle = tkFont.Font(size=20)
window.title('房租管理介面')
window.geometry('800x600')
window.configure(background='white')
"""def ClickMe():
    print(room_label.current())
    global other_charge
    global rent
    global other
    index = room_label.current()
    df = pd.read_csv('/Users/raindy/Downloads/房租計算表-2.csv')
    # 顯示房別
    label1.config(text=df.房別[index])
    # 顯示租金與其他費用
    parking = df.停車費用[index]
    print('parking', parking)
    add_person = df.加人費用[index]
    print('add_person', add_person)
    rent, other_charge = df.使用租金[index], parking + add_person
    print('other_charge', other_charge)
    other = ''
    # 衡量是否需要顯示其他費用
    if parking + add_person == 0:
        print('parking + add_person == 0 ')
        pass
    elif parking > 0 and add_person == 0:
        print('parking > 0 and add_person == 0')
        other = '3. 停車費用為' + str(parking) + '元。\n'
    elif parking == 0 and add_person > 0:
        print('parking == 0 and add_person > 0 ')
        other = '3. 加人費用為' + str(add_person) + '元。\n'
    elif parking > 0 and add_person > 0:
        print('parking > 0 and add_person > 0 ')
        other = '3. 停車費用為' + str(parking) + '元，以及加人費用為' + str(add_person) + '元。\n'
    return
"""
room_list = tuple(df.房別)
time_label = tk.Label(window, text='時間', bg="white", fg="black", font=fontStyle)
time_label.grid(column=2, row=3, ipadx=15, pady=10)
time_frame = tk.Frame(window)
time_entry = tk.Entry(window, width=20)
time_entry.grid(column=3, row=3, ipadx=15, pady=10)
d = datetime.date.today()
#這裡我也有加
today_date = d.day
tomorrow = today_date + 1
tomorrow2 = today_date + 2
print(d.day, tomorrow, tomorrow2)
### 計算房租介面 ###
# 介面名稱
#header_label = tk.Label(window, text='計算房租介面', bg="white", fg="gray", font=fontStyle)
#header_label.grid(column=1, row=3, ipadx=15, pady=10)
# 第三列為選擇房號
# # room_frame = tk.Frame(window)
room_label = tk.Label(window, text='選擇房號', bg="white", fg="black", font=fontStyle)
room_label.grid(column=2, row=8, ipadx=15, pady=10)
label1 = ttk.Label(window, text="請選擇", font=fontStyle)
label1.grid(column=6, row=8)
room_label = tk.Label(window, text='下拉選項', bg="white", fg="black", font=fontStyle)
room_label = ttk.Combobox(window)
room_label['value'] = room_list
room_label.grid(column=3, row=8, ipadx=15, pady=10)

##我從這裡開始打
header_label = tk.Label(window, text='待收房租',bg="white", fg="gray", font=fontStyle)
header_label.grid(column=1, row=13, ipadx=15, pady=10)

date_list = tuple(df.固定繳費日)
#顯示今天要繳房租的戶名
if d.day in date_list:
    print(date_list.count(d.day))
    today_count = date_list.count(d.day)
    today_count_index = []
    for j in range(18):
        if d.day == date_list[j]:
            today_count_index.append(j)
    for i in range(today_count):
        index_today = today_count_index[i]
        room__pay_today = tk.Label(window, text= room_list[index_today], bg="white", fg="black", font=fontStyle)
        room__pay_today.grid(column=3, row=18+5*i, ipadx=15, pady=10)
    today_pay_buttom = 18+5*today_count
else:
    no_rent = tk.Label(window, text='沒有待收房租', bg="white", fg="black", font=fontStyle)
    no_rent.grid(column=3, row=18, ipadx=15, pady=10)

#顯示明天要繳房租的戶名
if tomorrow in date_list:
    tomorrow_count = date_list.count(tomorrow)
    tomorrow_count_index = []
    for j in range(18):
        if tomorrow == date_list[j]:
            tomorrow_count_index.append(j)
    for i in range(tomorrow_count):
        index_tomorrow = tomorrow_count_index[i]
        room__pay_tomorrow = tk.Label(window, text= room_list[index_tomorrow], bg="white", fg="black", font=fontStyle)
        room__pay_tomorrow.grid(column=3, row=today_pay_buttom+5*i, ipadx=15, pady=10)
    tomorrow_pay_buttom = today_pay_buttom+5*tomorrow_count
else:
    no_rent = tk.Label(window, text='沒有待收房租', bg="white", fg="black", font=fontStyle)
    no_rent.grid(column=3, row=18+5*(today_count), ipadx=15, pady=10)

#顯示後天要繳房租的戶名
if tomorrow2 in date_list:
    tomorrow2_count = date_list.count(tomorrow2)
    tomorrow2_count_index = []
    for j in range(18):
        if tomorrow2 == date_list[j]:
            tomorrow2_count_index.append(j)
    for i in range(tomorrow2_count):
        index_tomorrow2 = tomorrow2_count_index[i]
        room__pay_tomorrow2 = tk.Label(window, text= room_list[index_tomorrow2], bg="white", fg="black", font=fontStyle)
        room__pay_tomorrow2.grid(column=3, row=tomorrow_pay_buttom+5*i, ipadx=15, pady=10)
else:
    no_rent = tk.Label(window, text='沒有待收房租', bg="white", fg="black", font=fontStyle)
    no_rent.grid(column=3, row=18+5*(tomorrow_count), ipadx=15, pady=10)

day_label1 = tk.Label(window, text='今天', bg="white", fg="black", font=fontStyle)
day_label1.grid(column=2, row=18, ipadx=15, pady=10)
day_label2 = tk.Label(window, text='明天', bg="white", fg="black", font=fontStyle)
day_label2.grid(column=2, row=23, ipadx=15, pady=10)
day_label2 = tk.Label(window, text='後天', bg="white", fg="black", font=fontStyle)
day_label2.grid(column=2, row=28, ipadx=15, pady=10)
#label1 = ttk.Label(window, text="請選擇", font=fontStyle)
#label1.grid(column=6, row=8)
'''
day_label1 = tk.Label(window, text='下拉選項', bg="white", fg="black", font=fontStyle)
day_label1 = ttk.Combobox(window)
day_label1['value'] = room_list
day_label1.grid(column=3, row=8, ipadx=15, pady=10)
'''





# 選完確定按鈕
#action = ttk.Button(window, text="確認", command=ClickMe)
action = ttk.Button(window, text="確認")
action.grid(column=5, row=8, ipadx=15, pady=10)
window.mainloop()
