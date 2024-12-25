from tkinter import *
import random
import time

def clear_frame(frame):
    # 清除指定 Frame 中的所有子部件
    for widget in frame.winfo_children():
        widget.destroy()

# 翻牌逻辑
def flip_card(btn, card_index):
    global first_card, second_card, buttons, card_values, matched_pairs

    # 如果按钮已经翻开，直接返回
    if btn["text"] != "?":
        return

    # 显示卡片内容
    btn["text"] = card_values[card_index]

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
        else:
            # 不匹配，翻回去
            first_card[0]["text"] = "?"
            second_card[0]["text"] = "?"

        # 重置
        first_card = None
        second_card = None

        # 检查胜利条件
        if matched_pairs == len(card_values) // 2:
            win_label = Label(fr1, text="你赢了！", font=("Arial", 24), fg="green")
            win_label.grid(row=3, column=1, columnspan=2, pady=10)

# 游戏开始
def start():
    global first_card, second_card, buttons, card_values, matched_pairs

    # 初始化全局变量
    first_card = None
    second_card = None
    matched_pairs = 0

    # 清空旧的卡片
    clear_frame(fr2)

    try:
        num_cards = int(entry.get())
        if num_cards % 2 != 0 or num_cards < 2:
            print("请输入一个大于2的偶数！")
            return

        # 生成随机的配对内容
        card_values = list(range(1, num_cards // 2 + 1)) * 2
        random.shuffle(card_values)

        # 创建按钮
        buttons = []
        rows = num_cards // 10
        extra_cols = num_cards % 10

        for i in range(rows):
            for j in range(10):
                btn = Button(fr2, text="?", width=7, height=4, 
                             command=lambda b=len(buttons): flip_card(buttons[b], b))
                btn.grid(row=i, column=j, padx=5, pady=5)
                buttons.append(btn)

        for k in range(extra_cols):
            btn = Button(fr2, text="?", width=7, height=4, 
                         command=lambda b=len(buttons): flip_card(buttons[b], b))
            btn.grid(row=rows, column=k, padx=5, pady=5)
            buttons.append(btn)

    except ValueError:
        print("请输入有效的数字！")

# 主窗口
root = Tk()
root.title("卡牌配对游戏")
root.geometry("700x900")

# 上方设置区
fr1 = Frame(root)
fr1.pack(fill='x')

Label(fr1, text="卡牌数量(需为偶数):").grid(row=0, column=0, padx=10)
entry = Entry(fr1)
entry.grid(row=0, column=1)
Button(fr1, text="开始游戏", command=start).grid(row=0, column=2, ipadx=20)

# 卡牌区
fr2 = Frame(root)
fr2.pack()

root.mainloop()
