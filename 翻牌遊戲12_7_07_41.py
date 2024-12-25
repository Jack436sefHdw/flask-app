from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import random
import time

# def update_timer():
#     global start_time, labtime1

#     if start_time is not None:
#         elapsed_time = int(time.time() - start_time)
#         minutes = elapsed_time // 60
#         seconds = elapsed_time % 60
#         lab1.config(text=f"計時配對時間:{minutes}:{seconds:02}")

#         # Continue updating the timer if the game is not over
#         if matched_pairs < len(card_values) // 2:
#             root.after(1000, update_timer)

def update_timer():
    global start_time, lab1, matched_pairs, card_values,page
    if page==1:
        if start_time is not None and matched_pairs < len(card_values) // 2:
            elapsed_time = int(time.time() - start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            lab1.config(text=f"計時配對時間:{minutes}:{seconds:02}",font=25)
            root.after(1000, update_timer)
        elif matched_pairs == len(card_values) // 2:
            elapsed_time = int(time.time() - start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            lab1.config(text=f"總時間:{minutes}:{seconds:02}",font=25)
    elif page==2:
        if start_time is not None and matched_pairs < len(card_values) // 2:
            elapsed_time = int(time.time() - start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            lab2_1.config(text=f"計時配對時間:{minutes}:{seconds:02}",font=25)
            root.after(1000, update_timer)
        elif matched_pairs == len(card_values) // 2:
            elapsed_time = int(time.time() - start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            lab2_1.config(text=f"總時間:{minutes}:{seconds:02}",font=25)


def load_images():
    global images , is_54
    """加载所有卡片图片并存储在字典中"""
    suits = ["心", "桃", "菱", "梅"]
    images = {}
    for suit in suits:
        for number in range(1, 14):  # 1-13号卡片
            file_name = f"{suit}{number}.png"
            try:
                images[f"{suit}{number}"] = PhotoImage(file=file_name)
            except Exception as e:
                print(f"Error loading image {file_name}: {e}")
    if is_54:
        images["醜0"] = PhotoImage(file="醜0.png")
        images["丑0"] = PhotoImage(file="丑0.png")
    return images

def check_match():
    global first_card, second_card, buttons, card_values, matched_pairs, is_flipping

    first_card_value = card_values[first_card[1]][1:]
    second_card_value = card_values[second_card[1]][1:]

    if first_card_value == second_card_value:
        matched_pairs += 1
        first_card[0]["state"] = "disabled"
        second_card[0]["state"] = "disabled"
    else:
        # Flip back the cards
        first_card[0].config(image=back_image)
        first_card[0].image_shown = False
        second_card[0].config(image=back_image)
        second_card[0].image_shown = False

    # Reset cards and allow new moves
    first_card = None
    second_card = None

    # Unset the flipping state
    is_flipping = False
    
    # Check if the game is won
    if matched_pairs == len(card_values) // 2:
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        if is_54 == True:
            messagebox.showinfo("恭喜", f"完成54張撲克牌配對，總翻牌次數：{flip_count}，使用時間為 {minutes}:{seconds:02}。要登入成績嗎?")
        else:
            messagebox.showinfo("恭喜", f"完成52張撲克牌配對，總翻牌次數：{flip_count}，使用時間為 {minutes}:{seconds:02}。要登入成績嗎?")

def flip_card(btn, card_index):
    global first_card, second_card, buttons, card_values, matched_pairs, flip_count,num
    
    # 如果按钮已经翻开，直接返回
    if btn["text"] != "?":
        return

    # 显示卡片内容
    btn["text"] = card_values[card_index]
    
    flip_count += 1
    lab2.config(text=f"計算翻牌次數:{flip_count}")

    # 如果是第一张卡
    if first_card is None:
        first_card = (btn, card_index)
    elif second_card is None:  # 如果是第二张卡
        second_card = (btn, card_index)

        # 检查是否匹配
        root.update()  # 强制刷新界面以显示翻开的卡
        time.sleep(0.5)  # 增加短暂延迟以便玩家看到结果

        if card_values[first_card[1]] == card_values[second_card[1]]:
            # 匹配成功
            matched_pairs += 1
            first_card[0]["state"] = "disabled"
            second_card[0]["state"] = "disabled"
            # first_card[0].destroy()
            # second_card[0].destroy()
        else:
            # 不匹配，翻回去
            first_card[0]["text"] = "?"
            second_card[0]["text"] = "?"

        # 重置
        first_card = None
        second_card = None

        # 检查胜利条件
        if matched_pairs == len(card_values) // 2:
            clear_frame(fr2)
            clear_frame(fr3)
            win_label = Label(fr3, text="你赢了！", font=("Arial", 24))
            win_label.grid(row=3, column=2, columnspan=2, pady=10)
        
            # 計算遊戲時間
            elapsed_time = int(time.time() - start_time)
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            card_score=int((1-0.9*(flip_count-num)/num)*100*num)
            time_score=int((1-0.5*(elapsed_time-num*2)/num*2)*100*num)
            print(f'翻牌分數:{card_score}')
            print(f'時間分數:{time_score}')
            
            # 顯示訊息框，詢問是否登入成績，加入 num
            response = messagebox.askquestion(
                "詢問",
                f"你選擇的卡牌數量為 {num}，翻牌的次數為 {flip_count}，使用時間為 {minutes}:{seconds:02}。要登入成績嗎?"
            )
            if response == "yes":
                print("用戶選擇了是")
                # 可以在這裡添加登入成績的邏輯
            else:
                print("用戶選擇了否")

def flip_playcard(btn, card_index):
    global first_card, second_card, buttons, card_values, matched_pairs, flip_count, is_flipping ,images

    # Return if the card is already shown or if another match is being checked
    if btn.image_shown or is_flipping:
        return

    btn.config(image=images[card_values[card_index]])
    btn.image_shown = True
    flip_count += 1
    lab2_2.config(text=f"計算翻牌次數:{flip_count}",font=25)

    if first_card is None:
        first_card = (btn, card_index)
    elif second_card is None:
        second_card = (btn, card_index)
        is_flipping = True  # Set the flipping state to True
        root.after(500, check_match)  # 延遲檢查匹配

def start_playcard():
    global buttons, card_values, matched_pairs, flip_count, start_time, first_card, second_card, is_flipping,images,back_image ,is_54,page
    buttons = []
    page=2
    first_card = None
    second_card = None
    matched_pairs = 0
    flip_count = 0
    start_time = time.time()
    lab2_1.config(text="計時配對時間:0:00",font=25)
    lab2_2.config(text="計算翻牌次數:0",font=25)
    clear_frame(fr2_2)
    clear_frame(fr2_3)
    selection = var.get()
    is_flipping = False
    #print(selection)
    back_image = PhotoImage(file="back.png")
    
    if selection == "52張":
        is_54=False
        card_values = random.sample(
            [f"{suit}{number}" for suit in ["心", "桃", "菱", "梅"] for number in range(1, 14)],52)
        random.shuffle(card_values)

        for i in range(5):
            for j in range(10):
                idx = i * 10 + j
                btn = Button(fr2_2, image=back_image, command=lambda b=idx: flip_playcard(buttons[b], b))
                btn.grid(row=i, column=j, padx=1, pady=2)
                btn.image_shown = False
                buttons.append(btn)

        for k in range(2):  # 新增的卡片顯示在第六行
            idx = 50 + k
            btn = Button(fr2_3, image=back_image, command=lambda b=idx: flip_playcard(buttons[b], b))
            btn.grid(row=0, column=k, padx=1, pady=2)
            btn.image_shown = False
            buttons.append(btn)
    else:
        is_54=True
        card_values = random.sample(
            [f"{suit}{number}" for suit in ["心", "桃", "菱", "梅"] for number in range(1, 14)] + ["醜0", "丑0"],54)
        random.shuffle(card_values)
        for i in range(5):
            for j in range(10):
                idx = i * 10 + j
                btn = Button(fr2_2, image=back_image, command=lambda b=idx: flip_playcard(buttons[b], b))
                btn.grid(row=i, column=j, padx=1, pady=2)
                btn.image_shown = False
                buttons.append(btn)
        for k in range(4):  # 新增的卡片顯示在第六行
            idx = 50 + k
            btn = Button(fr2_3, image=back_image, command=lambda b=idx: flip_playcard(buttons[b], b))
            btn.grid(row=0, column=k, padx=1, pady=2)
            btn.image_shown = False
            buttons.append(btn)
    images = load_images() 
    update_timer() 

    
def start_numder():
    global first_card, second_card, buttons, card_values, matched_pairs, flip_count, start_time,num,page
    
    # 初始化全局变量
    page=1
    buttons = []
    first_card = None
    second_card = None
    matched_pairs = 0
    flip_count = 0
    start_time = time.time()
    lab1.config(text="計時配對時間:0:00",font=25)
    lab2.config(text="計算翻牌次數:0",font=25)
    clear_frame(fr2)
    clear_frame(fr3)
    try:
        num = int(entry.get())  # 將輸入轉換為整數
    except ValueError:
        messagebox.showerror("錯誤", "要輸入數字")
        entry.delete(0,END)
    if num <= 2:
        messagebox.showerror("錯誤", "數字要大於2")
        entry.delete(0,END)
    elif num  > 100 :
        messagebox.showerror("錯誤", "數字要小於等於100")
        entry.delete(0,END)
    elif num % 2 != 0:
        messagebox.showerror("錯誤", "數字要是偶數")
        entry.delete(0,END)
    else:
        closest_factors = None  # 儲存因數對
        min_diff = float('inf')  # 初始化最小差距為無窮大
        
        card_values = list(range(1, num // 2 + 1)) * 2
        random.shuffle(card_values)
        
        for l in range(1, int(num**0.5) + 1):  # 只需要檢查到 num 的平方根
            if num % l == 0:  # 如果 l 是因數
                il = num // l  # 計算另一個因數
                diff = abs(il - l)  # 計算因數差距的絕對值
                if diff < min_diff:  # 如果找到更小的差距
                    min_diff = diff
                    closest_factors = (l, il)  # 更新最近的因數對
        
        # 格式化輸出
        if closest_factors and closest_factors[0] <= 10 and closest_factors[1] <= 10:
            #print(f"{num} = {closest_factors[0]} X {closest_factors[1]}")
            for i in range(closest_factors[0]):
                for l in range(closest_factors[1]):
                    btn = Button(fr2, text="?", width=7, padding=(1, 24), command=lambda b=len(buttons): flip_card(buttons[b], b))
                    btn.grid(row=i, column=l, padx=5, pady=5)
                    buttons.append(btn)
                    
        elif closest_factors and (closest_factors[0] > 10 or closest_factors[1] > 10):
            #print(f"{num} = {closest_factors[0]} X {closest_factors[1]}")
            for i in range(num // 10):
                for l in range(10):
                    btn = Button(fr2, text="?", width=7, padding=(1, 24), command=lambda b=len(buttons): flip_card(buttons[b], b))
                    btn.grid(row=i, column=l, padx=5, pady=5)
                    buttons.append(btn)
            for k in range(num % 10):
                btn = Button(fr3, text="?", width=7, padding=(1, 24), command=lambda b=len(buttons): flip_card(buttons[b], b))
                btn.grid(row=0, column=k, padx=5, pady=5)
                buttons.append(btn)
        #print(buttons)
        update_timer()

def clear_frame(frame):
    # 清除指定 Frame 中的所有子部件
    for widget in frame.winfo_children():
        widget.destroy()

root = Tk()
root.title("卡片配對")
root.geometry("690x900")

notebook = Notebook()

page=1

#第1頁頭
frame1 = Frame()
fr1_1 = Frame(frame1)
fr1_1.pack(fill='x')
labnum = Label(fr1_1, text="卡牌數量(大於2且小於等於100的偶數):",font=25)
labnum.grid(row=0, column=0, padx=10)
entry = Entry(fr1_1,font=25)
entry.grid(row=0, column=1)
lab1 = Label(fr1_1, text="計時配對時間:0:00",font=25)
lab1.grid(row=1, column=0)
lab2 = Label(fr1_1, text="計算翻牌次數:0",font=25)
lab2.grid(row=1, column=1)
startbtn = Button(fr1_1, text="開始", command=start_numder)
startbtn.grid(row=2, column=2, ipadx=20)
fr2 = Frame(frame1)
fr2.pack()
fr3 = Frame(frame1)
fr3.pack()
#第1頁尾

#第2頁頭
frame2 = Frame()
fr2_1 = Frame(frame2)
fr2_1.pack(fill='x')
images = {}
style = Style()
style.configure("Custom.TRadiobutton", font=("Arial", 13))  # 這裡字型不指定，字體大小設為25
labplaycard= Label(fr2_1, text="\t精神衰落:\t\t",font=25)
labplaycard.grid(row=0, column=0, padx=10)
var = StringVar(value="52張")

rb1 = Radiobutton(fr2_1, text="52張", variable=var, value="52張",style="Custom.TRadiobutton")
rb1.grid(row=0,column=1)
rb2 = Radiobutton(fr2_1, text="54張", variable=var, value="54張",style="Custom.TRadiobutton")
rb2.grid(row=0,column=2)
    
lab2_1 = Label(fr2_1, text="計時配對時間:0:00",font=25)
lab2_1.grid(row=1, column=0)
lab2_2 = Label(fr2_1, text="計算翻牌次數:0",font=25)
lab2_2.grid(row=1, column=1)
startbtn = Button(fr2_1, text="開始", command=start_playcard)
startbtn.grid(row=2, column=2, ipadx=20)
fr2_2 = Frame(frame2)
fr2_2.pack()
fr2_3 = Frame(frame2)
fr2_3.pack()
#第2頁尾


#第3頁頭
frame3 = Frame()
fr3_1 = Frame(frame3)
fr3_1.pack(fill='x')
#第3頁尾
notebook.add(frame1, text="數字")
notebook.add(frame2, text="撲克牌")
notebook.add(frame3, text="3")
notebook.pack(fill=BOTH, expand=True)

root.mainloop()
