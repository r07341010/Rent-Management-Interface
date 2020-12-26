import tkinter as tk
from tkinter import ttk  # 导入ttk模块，因为下拉菜单控件在ttk中
import tkinter.font as tkFont
import pandas as pd
import datetime
from tkcalendar import Calendar

calculate_file_path = 'C:\\Users\\johnc\\Desktop\\\房租計算表.csv'
calculate_file_path2 = 'C:\\Users\\johnc\\Desktop\\收租明細表.csv'

df = pd.read_csv(calculate_file_path, encoding='utf-8')
df2 = pd.read_csv(calculate_file_path2, encoding='utf-8')

gui1 = tk.Tk()
fontStyle1 = tkFont.Font(size=10, family='微軟正黑體')
fontStyle2 = tkFont.Font(size=12, family='微軟正黑體')
fontStyle3 = tkFont.Font(size=15, family='微軟正黑體')
gui1.title('首頁')
gui1.geometry('600x800')
gui1.configure(background='white')
room_list = tuple(df.房別)
d = datetime.date.today()

def Date(label, win):  # 這個函式首頁也可以用
    def ChooseDate():
        label.configure(text=str(cal.selection_get()).replace('-', '/'))
        top.destroy()
    top = tk.Toplevel(win)
    top.title('')
    cal = Calendar(top, selectmode='day', year=2020, month=12, day=25)
    cal.pack(fill="both", expand=True)
    ttk.Button(top, text="選取", command=ChooseDate).pack()

def ChooseRoom():
    roomindex = room_choice.current()
    if roomindex != -1:
        # 介面二
        window = tk.Toplevel(gui1)
        window.title('房租管理介面')
        window.geometry('800x600')
        window.configure(background='white')

        def CalculateRent():
            global df2
            global date
            
            def OK():
                result_window.destroy()
            
            if mouth_choice.current() != -1:
                time = str(mouth_choice.current() + 1) + '月'
                previous = float(previous_entry.get())
                month = float(month_entry.get())
                power = round(month - previous, 2)
                parking = df.loc[roomindex, '停車費用']
                add_person = df.loc[roomindex, '加人費用']
                rent = df.loc[roomindex, '使用租金']
                other_charge = parking + add_person
                if parking + add_person == 0 :
                    other = ''
                elif parking > 0 and add_person == 0 :
                    other = '3. 停車費用為'+str(parking)+'元。\n'
                elif parking == 0 and add_person > 0 :
                    other = '3. 加人費用為'+str(add_person)+'元。\n'
                elif parking > 0 and add_person > 0 :
                    other = '3. 停車費用為'+str(parking)+'元，以及加人費用為'+str(add_person)+'元。\n'

                if len(other) > 0: # 有其他費用：停車費或加人費用
                    # calculate the ouput content
                    pay = rent + power*5 + other_charge
                    head = '親愛的' + df.loc[roomindex, '房別'] + '房客您好，本期({:>})的房租費用'.format(time)
                    total = '總計{:<8}元，其中包含：\n'.format(format(pay,',')) # 千分位處理
                    rent_show = '1.租金{:<8}元\n'.format(format(rent,',')) # 千分位處理
                    power = '2.電費：本月耗電 {:<.1f} 度，小計 {:<.1f} 元。(上個月為 {:<.1f} 度電，本月為{:<.1f} 度電。)\n'.format(power,power*5,previous,month)
                    # print the output
                    result = head + total + rent_show + power + other
                else: # 無其他費用：停車費或加人費用
                    # calculate the ouput content
                    pay = rent + power*5
                    head = '親愛的' + df.loc[roomindex, '房別'] + '房客您好，本期({:>})的房租費用'.format(time)
                    total = '總計{:<8}元，其中包含：\n'.format(format(pay,',')) # 千分位處理
                    rent_show = '1.租金{:<8}元\n'.format(format(rent,',')) # 千分位處理
                    power = '2.電費：本月耗電 {:<.1f} 度，小計 {:<.1f} 元。(上個月為 {:<.1f} 度電，本月為{:<.1f} 度電。)\n'.format(power,power*5,previous,month)
                    # print the output
                    result = head + total + rent_show + power
                if roomindex in list_53 :# 如果是53號公寓
                    warning = '*** 小叮嚀：夜歸辛苦靜悄悄，垃圾分類請做好。 ***'
                    result = result + warning
                else:
                    pass
                
                # 更新 entry
                previous_entry.delete(0, 'end')
                month_entry.delete(0, 'end')
                
                # 更改前端
                mouth_choice.set('')
                inf9_label.configure(text=str(int(pay)) + '元', fg='black')
                
                # 更改後端
                df2.loc[roomindex, '總房租'] = pay
                tmpdf2 = pd.DataFrame(df2)
                tmpdf2.to_csv(calculate_file_path2, encoding='utf-8-sig', index=False)
                df2 = pd.read_csv(calculate_file_path2, encoding='utf-8')
                
                # 介面顯示結果
                result_window = tk.Toplevel(window)
                result_window.title('訊息')
                result_window.configure(background='white')
                result_label = tk.Label(result_window, text=result, bg='white', font=fontStyle1)
                result_label.grid(column=0, row=0, ipadx=5, pady=5, rowspan=5, columnspan=10, sticky='W')
                
                # 好 按鈕
                okbtt = ttk.Button(result_window, text="確認", width=8, command=OK)
                okbtt.grid(column=5, row=5, ipadx=5, pady=5, sticky='W')
                
                # automatically copy the output
                r = tk.Tk()
                r.withdraw()
                r.clipboard_clear()
                r.clipboard_append(result)
                r.destroy()
            
        
        
        def ChangeRent():
            global df
            def ChangeRent_inside():
                print('here')
                global df
                df.loc[roomindex, '使用租金'] = float(rent_entry_change.get()) if rent_entry_change.get() != '' else df.loc[roomindex, '使用租金']
                df.loc[roomindex, '停車費用'] = float(parking_entry_change.get()) if parking_entry_change.get() != '' else df.loc[roomindex, '停車費用']
                df.loc[roomindex, '加人費用'] = float(add_entry_change.get()) if add_entry_change.get() != '' else df.loc[roomindex, '加人費用']
                df.loc[roomindex, '固定繳費日'] = int(payday_entry_change.get()) if payday_entry_change.get() != '' else df.loc[roomindex, '固定繳費日']
                df.loc[roomindex, '聯絡電話'] = str(phone_entry_change.get()) if phone_entry_change.get() != '' else df.loc[roomindex, '聯絡電話']
                df.loc[roomindex, '姓名'] = str(name_entry_change.get()) if name_entry_change.get() != '' else df.loc[roomindex, '姓名']
                df.loc[roomindex, '身分證字號'] = str(id_entry_change.get()) if id_entry_change.get() != '' else df.loc[roomindex, '身分證字號']
                
                # 更改房客資料
                inf1_label_change.configure(text=df.loc[roomindex, '姓名'])
                inf1_label.configure(text=df.loc[roomindex, '姓名'])
                inf2_label_change.configure(text='0' + str(df.loc[roomindex, '聯絡電話']).lstrip('0'))
                inf2_label.configure(text='0' + str(df.loc[roomindex, '聯絡電話']).lstrip('0'))
                inf3_label_change.configure(text=str(df.loc[roomindex, '身分證字號']))
                inf3_label.configure(text=str(df.loc[roomindex, '身分證字號']))
                inf4_label_change.configure(text=str(int(df.loc[roomindex, '固定繳費日']))+'日')
                inf4_label.configure(text=str(int(df.loc[roomindex, '固定繳費日']))+'日')
                inf5_label_change.configure(text=str(int(df.loc[roomindex, '使用租金']))+'元')
                inf5_label.configure(text=str(int(df.loc[roomindex, '使用租金']))+'元')
                inf6_label_change.configure(text=str(int(df.loc[roomindex, '停車費用']))+'元')
                inf6_label.configure(text=str(int(df.loc[roomindex, '停車費用']))+'元')
                inf7_label_change.configure(text=str(int(df.loc[roomindex, '加人費用']))+'元')
                inf7_label.configure(text=str(int(df.loc[roomindex, '加人費用']))+'元')
                
                # 更新 entry
                name_entry_change.delete(0, 'end')
                phone_entry_change.delete(0, 'end')
                id_entry_change.delete(0, 'end')
                payday_entry_change.delete(0, 'end')
                rent_entry_change.delete(0, 'end')
                parking_entry_change.delete(0, 'end')
                add_entry_change.delete(0, 'end')
                
                # 更改後端
                tmpdf = pd.DataFrame(df)
                tmpdf.to_csv(calculate_file_path, encoding='utf-8-sig', index=False)
                df = pd.read_csv(calculate_file_path, encoding='utf-8')
                
                # 關閉介面
                gui_change_rent.destroy()
                
            ##
            
            gui_change_rent = tk.Toplevel(window)
            gui_change_rent.title('資料修改介面')
            gui_change_rent.geometry('300x300')
            gui_change_rent.configure(background='white')
            
            # 姓名
            title1_label_change = tk.Label(gui_change_rent, text='姓名：', bg="white", fg="black", font=fontStyle1)
            title1_label_change.grid(column=1, row=5, ipadx=5, pady=5)
            inf1_label_change = tk.Label(gui_change_rent, text=list(df.姓名)[roomindex], bg="white", fg="black", font=fontStyle1)
            inf1_label_change.grid(column=2, row=5, ipadx=5, pady=5, sticky='W')
            name_entry_change = tk.Entry(gui_change_rent, width=12)
            name_entry_change.grid(column=3, row=5, ipadx=5, pady=5, sticky='W', columnspan=2)
            
            # 聯絡電話
            title2_label_change = tk.Label(gui_change_rent, text='聯絡電話：', bg="white", fg="black", font=fontStyle1)
            title2_label_change.grid(column=1, row=6, ipadx=5, pady=5)
            inf2_label_change = tk.Label(gui_change_rent, text='0' + str(list(df.聯絡電話)[roomindex]), bg="white", fg="black", font=fontStyle1)
            inf2_label_change.grid(column=2, row=6, ipadx=5, pady=5, sticky='W')
            phone_entry_change = tk.Entry(gui_change_rent, width=12)
            phone_entry_change.grid(column=3, row=6, ipadx=5, pady=5, sticky='W', columnspan=2)
    
            # 身分證字號
            title3_label_change = tk.Label(gui_change_rent, text='身分證字號：', bg="white", fg="black", font=fontStyle1)
            title3_label_change.grid(column=1, row=7, ipadx=5, pady=5)
            inf3_label_change = tk.Label(gui_change_rent, text=list(df.身分證字號)[roomindex].lstrip(' '), bg="white", fg="black", font=fontStyle1)
            inf3_label_change.grid(column=2, row=7, ipadx=5, pady=5, sticky='W')
            id_entry_change = tk.Entry(gui_change_rent, width=12)
            id_entry_change.grid(column=3, row=7, ipadx=5, pady=5, sticky='W', columnspan=2)
    
            # 固定繳費日
            title4_label_change = tk.Label(gui_change_rent, text='固定繳費日：', bg="white", fg="black", font=fontStyle1)
            title4_label_change.grid(column=1, row=8, ipadx=5, pady=5)
            inf4_label_change = tk.Label(gui_change_rent, text=str(list(df.固定繳費日)[roomindex]) + '日', bg="white", fg="black", font=fontStyle1)
            inf4_label_change.grid(column=2, row=8, ipadx=5, pady=5, sticky='W')
            payday_entry_change = tk.Entry(gui_change_rent, width=12)
            payday_entry_change.grid(column=3, row=8, ipadx=5, pady=5, sticky='W', columnspan=2)
    
            # 使用租金
            title5_label_change = tk.Label(gui_change_rent, text='使用租金：', bg="white", fg="black", font=fontStyle1)
            title5_label_change.grid(column=1, row=9, ipadx=5, pady=5)
            inf5_label_change = tk.Label(gui_change_rent, text=str(list(df.使用租金)[roomindex]) + '元', bg="white", fg="black", font=fontStyle1)
            inf5_label_change.grid(column=2, row=9, ipadx=5, pady=5, sticky='W')
            rent_entry_change = tk.Entry(gui_change_rent, width=12)
            rent_entry_change.grid(column=3, row=9, ipadx=5, pady=5, sticky='W', columnspan=2)
    
            # 停車費用
            title6_label_change = tk.Label(gui_change_rent, text='停車費用：', bg="white", fg="black", font=fontStyle1)
            title6_label_change.grid(column=1, row=10, ipadx=5, pady=5)
            inf6_label_change = tk.Label(gui_change_rent, text=str(list(df.停車費用)[roomindex]) + '元', bg="white", fg="black", font=fontStyle1)
            inf6_label_change.grid(column=2, row=10, ipadx=5, pady=5, sticky='W')
            parking_entry_change = tk.Entry(gui_change_rent, width=12)
            parking_entry_change.grid(column=3, row=10, ipadx=5, pady=5, sticky='W', columnspan=2)
    
            # 加人費用
            title7_label_change = tk.Label(gui_change_rent, text='加人費用：', bg="white", fg="black", font=fontStyle1)
            title7_label_change.grid(column=1, row=11, ipadx=5, pady=5)
            inf7_label_change = tk.Label(gui_change_rent, text=str(list(df.加人費用)[roomindex]) + '元', bg="white", fg="black", font=fontStyle1)
            inf7_label_change.grid(column=2, row=11, ipadx=5, pady=5, sticky='W')
            add_entry_change = tk.Entry(gui_change_rent, width=12)
            add_entry_change.grid(column=3, row=11, ipadx=5, pady=5, sticky='W', columnspan=2)
            
            # 空白行 
            blank_label = tk.Label(gui_change_rent, text=' ', bg="white", fg="black", font=fontStyle1)
            blank_label.grid(column=1, row=12, ipadx=5, pady=1)
            
            # 按鈕
            changebtt = ttk.Button(gui_change_rent, text="更改資料",command=ChangeRent_inside, width=10)
            changebtt.grid(column=2, row=20, ipadx=10)#, pady=5)
            
            
            ##
            
        def ConfirmPay():
            global df2

            def OK2():
                not_window.destroy()
            
            if df2.loc[roomindex, '總房租'] == '未計算':
                not_window = tk.Toplevel(window)
                not_window.title('訊息')
                not_window.configure(background='white')
                not_label = tk.Label(not_window, text='房租尚未計算!', bg='white', font=fontStyle2)
                not_label.grid(column=0, row=0, ipadx=5, pady=5)

                ok2btt = ttk.Button(not_window, text="確認", width=8, command=OK2)
                ok2btt.grid(column=0, row=1, ipadx=5, pady=5)
                
            else:
                df2.loc[roomindex, '繳費狀態'] = '已繳'
                # 日期增加
                for i in range(5, 0, -1):
                    if i > 1:
                        curcolumn = '繳費日期' + str(i)
                        forecolumn = '繳費日期' + str(i - 1)
                        curcolumnp = '費用' + str(i)
                        forecolumnp = '費用' + str(i - 1)
                        df2.loc[roomindex, curcolumn] = df2.loc[roomindex, forecolumn]
                        df2.loc[roomindex, curcolumnp] = df2.loc[roomindex, forecolumnp]
                    if i == 1:
                        df2.loc[roomindex, '繳費日期1'] = date_label.cget('text')
                        df2.loc[roomindex, '費用1'] = df2.loc[roomindex, '總房租']
                tmpdf2 = pd.DataFrame(df2)
                tmpdf2.to_csv(calculate_file_path2, encoding='utf-8-sig', index=False)
                df2 = pd.read_csv(calculate_file_path2, encoding='utf-8')

                # 更改前端
                inf8_label.configure(text=str(list(df2.繳費狀態)[roomindex]), bg="white",
                                     fg="red" if str(list(df2.繳費狀態)[roomindex]) == '未繳' else 'green', font=fontStyle1)
                date_label.configure(text='')
                
                for i in range(5):
                    df2column = '繳費日期' + str(i + 1)
                    df2columnp = '費用' + str(i + 1)
                    if str(df2.loc[roomindex, df2column]) != 'nan':
                        trade1_label = tk.Label(window, text=str(df2.loc[roomindex, df2column]), bg="white", fg="black", font=fontStyle1)
                        trade1_label.grid(column=7, row=4 + i, ipadx=5, pady=5, sticky='W')
                        trade2_label = tk.Label(window, text=str(int(df2.loc[roomindex, df2columnp])) + ' 元', bg="white", fg="black", font=fontStyle1)
                        trade2_label.grid(column=8, row=4 + i, ipadx=5, pady=5, sticky='W')
                    else:
                        break

        def ResetPay():
            global df2
            if df2.loc[roomindex, '繳費狀態'] == '已繳':
                df2.loc[roomindex, '繳費狀態'] = '未繳'
                inf8_label.configure(text='未繳', bg="white", fg="red", font=fontStyle1)
                # 更改後端
                tmpdf2 = pd.DataFrame(df2)
                tmpdf2.to_csv(calculate_file_path2, encoding='utf-8-sig', index=False)
                df2 = pd.read_csv(calculate_file_path2, encoding='utf-8')

            inf9_label.configure(text='未計算', bg="white", fg="red", font=fontStyle1)
            df2.loc[roomindex, '總房租'] = '未計算'
            tmpdf2 = pd.DataFrame(df2)
            tmpdf2.to_csv(calculate_file_path2, encoding='utf-8-sig', index=False)
            df2 = pd.read_csv(calculate_file_path2, encoding='utf-8')

        list_53 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
        room_list = tuple(df.房別)

        '''global roomindex
        roomindex = 18  # 之後改成前一個介面選的房號'''

        '''房客資料'''
        title_label = tk.Label(window, text=str(df.loc[roomindex, '房別']) + '房客資料', bg="white", fg="grey", font=fontStyle2)
        title_label.grid(column=1, row=3, ipadx=5, pady=5, sticky='W', columnspan=2)

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
        inf3_label = tk.Label(window, text=list(df.身分證字號)[roomindex].lstrip(' '), bg="white", fg="black", font=fontStyle1)
        inf3_label.grid(column=2, row=6, ipadx=5, pady=5, sticky='W')

        # 固定繳費日
        title4_label = tk.Label(window, text='固定繳費日：', bg="white", fg="black", font=fontStyle1)
        title4_label.grid(column=1, row=7, ipadx=5, pady=5)
        inf4_label = tk.Label(window, text=str(list(df.固定繳費日)[roomindex]) + '日', bg="white", fg="black", font=fontStyle1)
        inf4_label.grid(column=2, row=7, ipadx=5, pady=5, sticky='W')

        # 使用租金
        title5_label = tk.Label(window, text='使用租金：', bg="white", fg="black", font=fontStyle1)
        title5_label.grid(column=1, row=8, ipadx=5, pady=5)
        inf5_label = tk.Label(window, text=str(int(list(df.使用租金)[roomindex])) + '元', bg="white", fg="black", font=fontStyle1)
        inf5_label.grid(column=2, row=8, ipadx=5, pady=5, sticky='W')

        # 停車費用
        title6_label = tk.Label(window, text='停車費用：', bg="white", fg="black", font=fontStyle1)
        title6_label.grid(column=1, row=9, ipadx=5, pady=5)
        inf6_label = tk.Label(window, text=str(int(list(df.停車費用)[roomindex])) + '元', bg="white", fg="black", font=fontStyle1)
        inf6_label.grid(column=2, row=9, ipadx=5, pady=5, sticky='W')

        # 加人費用
        title7_label = tk.Label(window, text='加人費用：', bg="white", fg="black", font=fontStyle1)
        title7_label.grid(column=1, row=10, ipadx=5, pady=5)
        inf7_label = tk.Label(window, text=str(int(list(df.加人費用)[roomindex])) + '元', bg="white", fg="black", font=fontStyle1)
        inf7_label.grid(column=2, row=10, ipadx=5, pady=5, sticky='W')

        # 更改資料
        changebtt1 = ttk.Button(window, text="更改資料", command=ChangeRent, width=7)
        changebtt1.grid(column=2, row=3, ipadx=5, pady=5, sticky='W')

        # 繳費狀態
        title8_label = tk.Label(window, text='繳費狀態：', bg="white", fg="black", font=fontStyle1)
        title8_label.grid(column=1, row=12, ipadx=5, pady=5)
        inf8_label = tk.Label(window, text=str(list(df2.繳費狀態)[roomindex]), bg="white", fg="red" if str(list(df2.繳費狀態)[roomindex]) == '未繳' else 'green', font=fontStyle1)
        inf8_label.grid(column=2, row=12, ipadx=5, pady=5, sticky='W')

        # 總租金
        title9_label = tk.Label(window, text='總租金(含電費)：', bg="white", fg="black", font=fontStyle1)
        title9_label.grid(column=1, row=11, ipadx=5, pady=5)
        try:
            inf9_label = tk.Label(window, text=str(int(float(df2.loc[roomindex, '總房租']))) + '元', bg="white",
                                  fg='black', font=fontStyle1)
            
        except:
            inf9_label = tk.Label(window, text=str(df2.loc[roomindex, '總房租']), bg="white",
                                  fg="red", font=fontStyle1)
        inf9_label.grid(column=2, row=11, ipadx=5, pady=5, sticky='W')

        # 重設繳費狀態
        resetbtt = ttk.Button(window, text="重設", width=7, command=ResetPay)
        resetbtt.grid(column=3, row=12, ipadx=5, pady=5, sticky='W')

        '''計算房租介面'''
        # 介面名稱
        header_label = tk.Label(window, text='計算總房租', bg="white", fg="grey", font=fontStyle2)
        header_label.grid(column=1, row=13, ipadx=5, pady=5, sticky='W')
        
        # 選取月份
        mouth_label = tk.Label(window, text='選取月份', bg="white", fg="black", font=fontStyle1)
        mouth_label.grid(column=1, row=14, ipadx=5, pady=5)
        mouth_choice = ttk.Combobox(window, width=10)
        mouth_choice['value'] = tuple(range(1, 13))
        mouth_choice.grid(column=2, row=14, ipadx=5, pady=5)
        
        # 前一月份電錶度數
        previous_label = tk.Label(window, text='前月電錶顯示(度)：',bg="white", fg="black", font=fontStyle1)
        previous_label.grid(column=1, row=15, ipadx=5, pady=5)
        previous_frame = tk.Frame(window)
        previous_entry = tk.Entry(window, width=10)
        previous_entry.grid(column=2, row=15, ipadx=5, pady=5)

        # 本月份電錶度數
        month_label = tk.Label(window, text='本月電錶顯示(度)：',bg="white", fg="black", font=fontStyle1)
        month_label.grid(column=1, row=16, ipadx=5, pady=5)
        month_frame = tk.Frame(window)
        month_entry = tk.Entry(window, width=10)
        month_entry.grid(column=2, row=16, ipadx=5, pady=5)

        # 計算按鈕
        global calculate_btn
        calculate_btn = tk.Button(window, text='計算本月房租', command=CalculateRent, fg="black", font=fontStyle1)
        calculate_btn.grid(column=3, row=16, ipadx=5, pady=5)

        '''確認繳費'''
        header2_label = tk.Label(window, text='繳費確認', bg="white", fg="grey", font=fontStyle2)
        header2_label.grid(column=1, row=18, ipadx=5, pady=5, sticky='W')
        
        # 選取日期
        datebtt = ttk.Button(window, text="選取日期", width=8, command=lambda: Date(date_label, window))
        datebtt.grid(column=1, row=19, ipadx=5, pady=5)
        global date_label
        date_label = tk.Label(window, text='', bg="white", fg="black", font=fontStyle1)
        date_label.grid(column=2, row=19, ipadx=5, pady=5, sticky='W')
        
        # 確認繳費按鈕
        confirmbtt = ttk.Button(window, text="確認繳費", width=8, command=ConfirmPay)
        confirmbtt.grid(column=3, row=19, ipadx=5, pady=5, sticky='W')
        
        '''前五筆交易資料'''
        # 介面名稱
        header2_label = tk.Label(window, text='過去五筆交易紀錄', bg="white", fg="grey", font=fontStyle2)
        header2_label.grid(column=7, row=3, ipadx=5, pady=5, sticky='W', columnspan=2)

        # 交易紀錄
        for i in range(5):
            df2column = '繳費日期' + str(i + 1)
            df2columnp = '費用' + str(i + 1)
            if str(df2.loc[roomindex, df2column]) != 'nan':
                trade1_label = tk.Label(window, text=str(df2.loc[roomindex, df2column]), bg="white", fg="black", font=fontStyle1)
                trade1_label.grid(column=7, row=4 + i, ipadx=5, pady=5, sticky='W')
                trade2_label = tk.Label(window, text=str(int(df2.loc[roomindex, df2columnp])) + ' 元', bg="white", fg="black", font=fontStyle1)
                trade2_label.grid(column=8, row=4 + i, ipadx=5, pady=5, sticky='W')
            else:
                trade1_label = tk.Label(window, text='無資料', bg="white", fg="black", font=fontStyle1)
                trade1_label.grid(column=7, row=4 + i, ipadx=5, pady=5, sticky='W')

        
        window.mainloop()

# 這裡我也有加
today_date = d.day
tomorrow = (d + datetime.timedelta(days=1)).day
tomorrow2 = (d + datetime.timedelta(days=2)).day

# 標題
gui1title1_label = tk.Label(gui1, text='選擇房號', bg="white", fg="grey", font=fontStyle3)
gui1title1_label.grid(column=1, row=5, ipadx=15, pady=5, sticky='W')

room_label = tk.Label(gui1, text='選擇房號：', bg="white", fg="black", font=fontStyle2)
room_label.grid(column=2, row=8, ipadx=15, pady=5)

room_choice = ttk.Combobox(gui1, width=10)
room_choice['value'] = tuple(df.房別)
room_choice.grid(column=3, row=8, ipadx=5, pady=5)

# 選完確定按鈕
action = ttk.Button(gui1, text="確認", width=5, command=ChooseRoom)
action.grid(column=4, row=8, ipadx=15, pady=5)

##我從這裡開始打
header_label = tk.Label(gui1, text='待收房租', bg="white", fg="gray", font=fontStyle3)
header_label.grid(column=1, row=13, ipadx=15, pady=5, sticky='W')

date_list = tuple(df.固定繳費日)
list_len = len(date_list)
# 顯示今天要繳房租的戶名
today_count = date_list.count(d.day)
if d.day in date_list:
    today_count_index = []
    for j in range(list_len):
        if d.day == date_list[j]:
            today_count_index.append(j)
    for i in range(today_count):
        index_today = today_count_index[i]
        room__pay_today = tk.Label(gui1, text=room_list[index_today], bg="white", fg="black", font=fontStyle2)
        room__pay_today.grid(column=3, row=18 + 5 * i, ipadx=15, pady=5, columnspan=2)
    today_pay_buttom = 18 + 5 * today_count
else:
    no_rent = tk.Label(gui1, text='沒有待收房租', bg="white", fg="black", font=fontStyle2)
    no_rent.grid(column=3, row=18, ipadx=15, pady=5, columnspan=2)
    today_pay_buttom = 18 + 5 * today_count

# 顯示明天要繳房租的戶名
tomorrow_count = date_list.count(tomorrow)
if tomorrow in date_list:
    tomorrow_count_index = []
    for j in range(list_len):
        if tomorrow == date_list[j]:
            tomorrow_count_index.append(j)
    for i in range(tomorrow_count):
        index_tomorrow = tomorrow_count_index[i]
        room__pay_tomorrow = tk.Label(gui1, text=room_list[index_tomorrow], bg="white", fg="black", font=fontStyle2)
        room__pay_tomorrow.grid(column=3, row=today_pay_buttom + 5 * i, ipadx=15, pady=5, columnspan=2)
    tomorrow_pay_buttom = today_pay_buttom + 5 * tomorrow_count
else:
    no_rent = tk.Label(gui1, text='沒有待收房租', bg="white", fg="black", font=fontStyle2)
    no_rent.grid(column=3, row=today_pay_buttom, ipadx=15, pady=5, columnspan=2)
    tomorrow_pay_buttom = today_pay_buttom + 5 * tomorrow_count

# 顯示後天要繳房租的戶名
tomorrow2_count = date_list.count(tomorrow2)
if tomorrow2 in date_list:
    tomorrow2_count_index = []
    for j in range(list_len):
        if tomorrow2 == date_list[j]:
            tomorrow2_count_index.append(j)
    for i in range(tomorrow2_count):
        index_tomorrow2 = tomorrow2_count_index[i]
        room__pay_tomorrow2 = tk.Label(gui1, text=room_list[index_tomorrow2], bg="white", fg="black", font=fontStyle2)
        room__pay_tomorrow2.grid(column=3, row=tomorrow_pay_buttom + 5 * i, ipadx=15, pady=5, columnspan=2)
else:
    no_rent = tk.Label(gui1, text='沒有待收房租', bg="white", fg="black", font=fontStyle2)
    no_rent.grid(column=3, row=tomorrow_pay_buttom, ipadx=15, pady=5, columnspan=2)

todaytext = d.strftime('%m/%d')
tomorrowtext = (d + datetime.timedelta(days=1)).strftime('%m/%d')
tomorrow2text = (d + datetime.timedelta(days=2)).strftime('%m/%d')

day_label1 = tk.Label(gui1, text=f'今天( {todaytext} )：', bg="white", fg="black", font=fontStyle2)
day_label1.grid(column=2, row=18, ipadx=15, pady=5)
day_label2 = tk.Label(gui1, text=f'明天( {tomorrowtext} )：', bg="white", fg="black", font=fontStyle2)
day_label2.grid(column=2, row=today_pay_buttom, ipadx=15, pady=5)
day_label3 = tk.Label(gui1, text=f'後天( {tomorrow2text} )：', bg="white", fg="black", font=fontStyle2)
day_label3.grid(column=2, row=tomorrow_pay_buttom, ipadx=15, pady=5)

gui1.mainloop()