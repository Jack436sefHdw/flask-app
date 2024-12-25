from tkinter import *
from tkinter.ttk import *
import random
import time

def update_timer():
    global start_time, labtime1

    if start_time is not None:
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        lab1.config(text=f"計時配對時間:{minutes}:{seconds:02}")

        # Continue updating the timer if the game is not over
        if matched_pairs < len(card_values) // 2:
            root.after(1000, update_timer)

def flip_card(btn, card_index):
    global first_card, second_card, buttons, card_values, matched_pairs, flip_count
    
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

def start():
    global first_card, second_card, buttons, card_values, matched_pairs, flip_count, start_time

    # 初始化全局变量
    buttons = []
    first_card = None
    second_card = None
    matched_pairs = 0
    flip_count = 0
    start_time = time.time()
    lab1.config(text="計時配對時間:0:00")
    lab2.config(text="計算翻牌次數:0")
    clear_frame(fr2)
    clear_frame(fr3)
    num = int(entry.get())  # 將輸入轉換為整數
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
        print(f"{num} = {closest_factors[0]} X {closest_factors[1]}")
        for i in range(closest_factors[0]):
            for l in range(closest_factors[1]):
                btn = Button(fr2, text="?", width=7, padding=(1, 24), command=lambda b=len(buttons): flip_card(buttons[b], b))
                btn.grid(row=i, column=l, padx=5, pady=5)
                buttons.append(btn)
                
    elif closest_factors and (closest_factors[0] > 10 or closest_factors[1] > 10):
        print(f"{num} = {closest_factors[0]} X {closest_factors[1]}")
        for i in range(num // 10):
            for l in range(10):
                btn = Button(fr2, text="?", width=7, padding=(1, 24), command=lambda b=len(buttons): flip_card(buttons[b], b))
                btn.grid(row=i, column=l, padx=5, pady=5)
                buttons.append(btn)
        for k in range(num % 10):
            btn = Button(fr3, text="?", width=7, padding=(1, 24), command=lambda b=len(buttons): flip_card(buttons[b], b))
            btn.grid(row=0, column=k, padx=5, pady=5)
            buttons.append(btn)
    update_timer()

def clear_frame(frame):
    # 清除指定 Frame 中的所有子部件
    for widget in frame.winfo_children():
        widget.destroy()

root = Tk()
root.title("卡片配對")
root.geometry("690x900")

notebook = Notebook()

frame1 = Frame()

frame2 = Frame()
frame3 = Frame()

fr1 = Frame(frame1)
fr1.pack(fill='x')
labnum = Label(fr1, text="卡牌數量(大於2且小於100的偶數):")
labnum.grid(row=0, column=0, padx=10)
entry = Entry(fr1)
entry.grid(row=0, column=1)
lab1 = Label(fr1, text="計時配對時間:0:00")
lab1.grid(row=1, column=0)
lab2 = Label(fr1, text="計算翻牌次數:0")
lab2.grid(row=1, column=1)

startbtn = Button(fr1, text="開始", command=start)
startbtn.grid(row=2, column=2, ipadx=20)

fr2 = Frame(frame1)
fr2.pack()

fr3 = Frame(frame1)
fr3.pack()

notebook.add(frame1, text="數字")
notebook.add(frame2, text="撲克牌")
notebook.add(frame3, text="麻將")
notebook.pack(fill=BOTH, expand=True)

root.mainloop()
